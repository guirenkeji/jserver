#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
from io import BytesIO
from docker import Client
import requests
from requests.exceptions import HTTPError
import traceback
import datetime
import uuid
import json
from docker_registry_client.docker_registry_client import DockerRegistryClient

logging.basicConfig(level=logging.DEBUG)

PULL_CMD = "docker pull"
USER = "dcos"
regisry_protocol = "http://"


def cmd_slave(url, data, request_timeout=10):
    try:
        logging.info('url = %s, data = %s, request_timeout = %s'%(url, data, request_timeout))
        r = requests.post(
            url, data=data, timeout=request_timeout,
            headers={'content-type': 'application/json'}
        )
        logging.info('return %s'%r.content)
        return r.status_code, json.loads(r.content)
    except Exception as e:
        logging.error(e)
        #logger.error("agent no ok")

@app.route("/prepublish", method='POST')
def pre_release():
    """
    image pre release request
    :return:
    """
    action_type = "镜像预发布"
    try:
        data = request.json
        logging.info('postdata = %s'%data)
        repo_name = data.get("imgName", None)
        version = data.get("version", None)
        username = data.get("userName", "")
        app_id = data.get("appId", "")
        logging.info("prepublish image_name {0} image version {1}".format(repo_name, version))
    except Exception as e:
        insert_sys_log(action_type, "admin", "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), "", result="预发布失败", lv="ERROR")
        logging.error(e)
        return {"st": "faild", "error_message":"请求参数格式错误, 镜像预发布失败"}
        #return HTTPResponse(status=200, body="request args invaild")

    try:
        if repo_name and version:
            if not dbapi.get_image_version(repo_name, version):
                insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), app_id,result="预发布失败", lv="ERROR")
                logging.error("prepublish image {0} version is None in db".format(repo_name, version))
                return {"st": "faild", "error_message":"镜像不存在, 镜像预发布失败"}

            image_url = "".join([repo_name, ":", version])
            logging.info("prepublish image_url {0}".format(image_url))
            query_image = "".join([repo_name, ":"])
            logging.info("query slaves image:{0}".format(query_image))
            hosts = get_app_slave(query_image)
            logging.info("prepublish slave nodes {0}".format(hosts))
            if not hosts:
                insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), app_id,result="预发布失败", lv="ERROR")
                logging.error("prepublish image_url slave nodes is None in db".format(image_url))
                return {"st": "failed", "error_message": "当前无应用使用该镜像，无需预发布"}
            cmd = "".join([PULL_CMD, " ", image_url])
            logging.info("prepublish pssh run cmd is  {0}".format(cmd))
            # pssh_slave(cmd, hosts)

            cmd_body = json.dumps({"cmd": cmd})
            for url in hosts:
                slave_url = "http://" + url + ":6061/v1.0/image/pull"
                logging.debug(slave_url)
                r_data = cmd_slave(slave_url, cmd_body)
                if r_data and r_data[0] == 200 and r_data[1]['st'] == 'ok':
                    logging.debug("%s pull ok" % slave_url)
                else:
                    logging.debug("%s pull not ok" % slave_url)
            insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布成功" % (repo_name, version), app_id,result="成功")
            return {"st": "ok", "message": "预发布成功"}
        else:
            insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), app_id,result="失败", lv="ERROR")
            logging.error("the prepublish image name or version is None...")
            return {"st": "failed", "error_message": "镜像名称或者版本为空, 镜像预发布失败"}
    except ValueError as e1:
        insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), app_id,result="失败", lv="ERROR")
        logging.error(e1)
        return {"st": "failed", "error_message": "请求参数解析错误, 镜像预发布失败"}
    except Exception as e2:
        insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像预发布失败" % (repo_name, version), app_id,result="失败", lv="ERROR")
        logging.error(e2)
        return {"st": "failed", "error_message": "服务内部错误, 镜像预发布失败"}

def insert_sys_log(action_type, user, info, app_id, result, lv="INFO", op_obj="Image" ):
    value = {
        "type": action_type,
        "username": user,
        "app_id": app_id,
        "result":result,
        "info": info,
        "time": datetime.datetime.now(),
        "lv": lv,
        "op_obj": op_obj,
        "seq": uuid.uuid1().get_hex()
    }
    dbapi.insert_sys_log(value)


def get_app_slave(image_url):
    logging.info('image_url = %s'%image_url)
    slave_hosts = []
    apps = dbapi.get_app_slaves(image_url)
    for _, _, app_info in apps:
        if app_info:
            slave_hosts.append(app_info.slave_ip)

    logging.info('return %s'%slave_hosts)
    return slave_hosts


@app.route("/:_image_name", method='POST')
def create_image(_image_name):
    # form_data = request.forms
    form_data = request.body.read()
    logging.info('postdata = %s'%form_data)
    # logging.debug("pre format Form data: %s" % form_data)
    form_data = json.loads(form_data)
    # logging.debug("Form data: %s" % form_data)

    image_id_input = form_data.get("imgId", None)
    image_name = form_data.get("imgName")
    type = form_data.get("imgType")
    info = form_data.get("imgInfo")
    app_name = form_data.get("appName", '')
    environment = form_data.get("environment")
    config_info = form_data.get("configInfo")
    username = form_data.get("userName")
    env = form_data.get("envVar")
    docker_file = form_data.get("docfile").replace('\\n', '\n').replace('\\r', '\r')

    create_at = datetime.datetime.now()
    version = create_at.strftime('%Y%m%d%H%M')

    cli = Client(base_url='unix://var/run/docker.sock' ,version="auto")
    f = BytesIO(docker_file.encode('utf-8'))

    tag = '%s:%s' % (image_name, version)

    try:
        db_handler = DBBaseHandler()
    except DBCertificationException as e:
        error_info = "DB auth error: %s" % e.message
        logging.error(error_info)
        return {
            'st': 'failed',
            'error_message': error_info
        }
    except DBConnectionException as e:
        error_info = "DB establish connection error: %s" % e.message
        logging.error(error_info)
        return {
            'st': 'failed',
            'error_message': error_info
        }
    except DBException as e:
        error_info = "DB error: %s" % e.message
        logging.error(error_info)
        return {
            'st': 'failed',
            'error_message': error_info
        }

    ret = _isImgNameDup(db_handler,image_name)
    if image_id_input is None and ret is not None:
        return {
                "st":"failed",
                "error_message":"创建镜像名称已经存在，请重新命名"
                }

    try:
        response = cli.build(fileobj=f, tag=tag)
        response_list = [line for line in response]
        resp = json.loads(response_list[-1])
        if not resp or not resp['stream'].startswith('Successfully built'):
            logging.exception("Occur some error when build image from dockerfile")
            error_message = '通过Dockerfile生成镜像时出错'
            _add_sys_log(db_handler, image_id_input, username, app_name, tag, error_detail=error_message)
            return {'st': 'failed', 'message': 'can\'t build image', 'detail': response_list[-1]}
    except Exception as e:
        error_info = "Occur some error when build image from dockerfile: %s" % e.message
        logging.error(error_info)
        error_message = '通过Dockerfile生成镜像时出错'
        _add_sys_log(db_handler, image_id_input, username, app_name, tag, error_detail=error_message)
        return {
            'st': 'failed',
            'error_message': error_info
        }

    version_id = uuid.uuid4()
    image_id = image_id_input if image_id_input else uuid.uuid4()
    version_info = {
        'img_name': image_name,
        'id': version_id,
        'version': version,
        'config_info': config_info,
        'docfile': docker_file,
        'status': 'ok',
        'deleted': 0,
        'created': create_at,
        'env': env
    }

    image_info = {
        'img_name': image_name,
        'img_type': type,
        'id': image_id,
        'img_info': info,
        'app_name': app_name,
        'environment': environment,
        'latest_version': version
    }


    try:
        push_response = cli.push(tag, stream=True)
        push_resp = [line for line in push_response]
        if 'errorDetail' in push_resp[-1]:
            error_message = "上传镜像到仓库失败,请确认镜像名称填写正确"
            _add_sys_log(db_handler, image_id_input, username, app_name, tag, error_detail=error_message)
            return {
                'st': 'failed',
                'error_message': error_message
            }
    except Exception as e:
        error_info = "Error occur when push image to registry repository: %s " % e.message
        logging.error(error_info)
        error_message = "上传镜像到仓库失败"
        _add_sys_log(db_handler, image_id_input, username, app_name, tag, error_detail=error_message)
        return {
            'st': 'failed',
            'error_message': error_info
        }

    try:
        db_handler = DBBaseHandler()
        if not image_id_input:
            _create_image_info(db_handler, image_info)
        _create_version_info(db_handler, version_info)
        _update_image_info(db_handler, image_id, version)
        _add_sys_log(db_handler, image_id_input, username, app_name, tag)
    except DBException as e:
        error_info = "DB error: %s" % e.message
        logging.error(error_info)
        error_message = "连接数据库时发生错误"
        _add_sys_log(db_handler, image_id_input, username, app_name, tag, error_detail=error_message)
        return {
            'st': 'failed',
            'error_message': error_info
        }

    return {
        'st': 'ok',
        'error_message': None
    }


def _create_image_info(db_handler, image_info):
    image_id = image_info['id']
    img_name = image_info['img_name']
    img_type = image_info['img_type']
    img_info = image_info['img_info']
    app_name = image_info['app_name']
    environment = image_info['environment']
    latest_version = image_info['latest_version']
    sql = "INSERT INTO image_info (id, img_name, img_type, img_info, app_name, version_count, latest_version, environment, deleted) VALUES " \
          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (image_id, img_name, img_type, img_info, app_name, 0, latest_version, environment, 0)
    db_handler.execute_sql(sql)


def _create_version_info(db_handler, version_info):
    id = version_info['id']
    img_name = version_info['img_name']
    version = version_info['version']
    config_info = version_info['config_info']
    docfile = version_info['docfile']
    status = version_info['status']
    deleted = version_info['deleted']
    created = version_info['created']
    env = version_info['env']
    sql = "INSERT INTO image_version_info (id, img_name, version, config_info, docfile, status, deleted, created, env) VALUES " \
          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (id, img_name, version, config_info, docfile, status, deleted, created, env)
    db_handler.execute_sql(sql)


def _update_image_info(db_handler, image_id, version):
    add_count_sql = "UPDATE image_info set version_count=version_count+1 WHERE id='%s'" % image_id
    db_handler.execute_sql(add_count_sql)

    update_version_sql = "UPDATE image_info set latest_version='%s' WHERE id='%s'" % (version, image_id)
    db_handler.execute_sql(update_version_sql)


def _get_image_id(db_handler, image_name):
    add_count_sql = "SELECT id FROM image_info WHERE img_name = '%s'" % image_name
    image_id = db_handler.execute_sql(add_count_sql).get('id')
    return image_id


def _add_sys_log(db_handler, image_id_input, user_name, app_name, tag, error_detail=None):
    seq_uuid = '%s' % uuid.uuid4()
    seq = seq_uuid.replace('-', '')

    type = '创建镜像版本' if image_id_input else '创建镜像'
    #type = '创建'
    # info = {
    #     'st': None,
    #     'error_message': None
    # }

    if not error_detail:
        # info['st'] = 'ok'
        info = '结果:成功, 版本信息: %s' %  tag
        result = type + "成功"
        lv = "INFO"
    else:
        # info['st'] = 'failed'
        # info['error_message'] = error_detail
        info = '结果:失败, 版本信息: %s' % tag
        result = type + "失败"
        lv = "ERROR"

    time = datetime.datetime.now()
    sql = "INSERT INTO sys_log (seq, type, time, username, info, lv, op_obj, app_id, result) VALUES" \
          "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (seq, type, time, user_name, info, lv, "image", app_name, result)
    #print(sql)
    db_handler.execute_sql(sql)

def _isImgNameDup(db_handler,imgName):
    """
    check imgName is or not duplicated
    """
    sql = 'SELECT DISTINCT "true" AS result FROM IMAGE_INFO WHERE IMG_NAME="%s" AND DELETED=0' % (imgName)
    ret = db_handler.execute_sql(sql)
    # print("=====check img name dup=======")
    # print(ret)
    return ret


@app.route("/version", method='DELETE')
def image_version_delete():
    """
    delete image version
    """
    action_type = "镜像版本删除"
    try:
        logging.info("delete data = {0}".format(request.body.read()))
        data = json.loads(request.body.read())
        repo_name = data.get("imgName", None)
        version = data.get("version", None)
        username = data.get("userName", None)
        app_id = data.get("appId", "")
        logging.info("delete image version image_name {0} version {1} username {2}".format(repo_name, version, username))
    except Exception as e:
        insert_sys_log(action_type, "admin", "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), "",result="删除失败", lv="ERROR")
        logging.error(e)
        return {"st": "failed", "error_message": "参数解析错误, 镜像版本删除失败"}

    try:
        if repo_name and version:
            if image_used(repo_name, version):
                insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), app_id,result="删除失败", lv="ERROR")
                logging.error("delete image {0} version {1} is used, not be delete".format(repo_name, version))
                return {"st": "failed", "error_message": "镜像版本正在使用, 无法删除，镜像版本删除失败"}

            if not dbapi.get_image_version(repo_name, version):
                insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), app_id,result="删除失败", lv="ERROR")
                logging.error("delete image {0} version {1} is not exist in db".format(repo_name, version))
                return {"st": "failed", "error_message": "镜像版本已经被删除"}

            delete_from_registry(repo_name, version)
            update_image_info(repo_name, version)
            insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除成功" % (repo_name, version), app_id,result="删除成功")
            return {"st": "ok"}
        else:
            insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), app_id,result="删除失败", lv="ERROR")
            logging.error("delete image {0} or version {1} is None".format(repo_name, version))
            return {"st": "failed", "error_message": "镜像名或版本为空， 镜像版本删除失败"}
    except ValueError as e1:
        insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), app_id,result="删除失败", lv="ERROR")
        logging.error(e1)
        return {"st": "failed", "error_message": "请求参数错误，镜像版本删除失败"}
    except Exception as e2:
        insert_sys_log(action_type, username, "镜像名称:%s 镜像版本:%s 结果描述:镜像版本删除失败" % (repo_name, version), app_id, result="删除失败",  lv="ERROR")
        logging.error(e2)
        #return HTTPResponse(status=500, body="interal server error")
        return {"st": "failed", "error_message": "服务器内部出错， 镜像版本删除失败"}


@app.route("/:name", method='DELETE')
def image_delete(name):
    """
    delete image all versions
    :return:
    """
    action_type = "镜像删除"
    try:
        logging.info("delete data = {0}".format(request.body.read()))
        data = json.loads(request.body.read())
        #logging.debug("delete image request body:{0}".format(request.body.read()))
        repo_name = data.get("imgName", None)
        username = data.get("userName", None)
        app_id = data.get("appId", "")
        #logger.info("delete image  image_name {0}  username {1}".format(repo_name, username))
    except Exception as e:
        insert_sys_log(action_type, "admin", "镜像名称:%s 结果描述:镜像删除失败" % repo_name, "",result="删除失败", lv="ERROR")
        logging.error(e)
        return {"st": "failed", "error_message": "请求参数错误， 镜像删除失败"}

    try:
        if repo_name:
            if image_used(repo_name):
                insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除失败, 镜像有版本正在使用" % repo_name, app_id,result="删除失败", lv="ERROR")
                logging.error("delete image {0} is used, not be delete".format(repo_name))
                return {"st": "failed", "error_message": "镜像正在使用，镜像删除失败"}

            images = dbapi.get_image_versions(repo_name)
            if not images:
                insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除失败, 镜像不存在" % repo_name, app_id,result="删除失败", lv="ERROR")
                logging.error("delete image {0} have no any versions in db".format(repo_name))
                return {"st": "failed", "error_message": "镜像已经被删除"}

            for image in images:
                version = image.version
                delete_from_registry(repo_name, version)
            update_image_info(repo_name)
            insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除成功" % repo_name, app_id,result="删除成功")
            return {"st": "ok"}
        else:
            insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除失败" % repo_name, app_id,result="删除失败", lv="ERROR")
            logging.error("delete image {0} is None in args".format(repo_name))
            return {"st": "failed", "error_message": "镜像名称为空,镜像删除失败"}
    except ValueError as e1:
        insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除失败" % repo_name, app_id,result="删除失败", lv="ERROR")
        logging.error(e1)
        return {"st": "failed", "error_message": "镜像删除失败"}
    except Exception as e2:
        insert_sys_log(action_type, username, "镜像名称:%s 结果描述:镜像删除失败" % repo_name, app_id,result="删除失败", lv="ERROR")
        logging.error(e2)
        return {"st": "failed", "error_message": "镜像删除失败"}
        #return HTTPResponse(status=500, body="interal server error")


def parse_repo(repo_name):
    """
    parse registry url and image name
    192.168.159.132:5000/ubuntu
    192.168.159.132:5000/library/ubuntu
    :param repo_name:
    :return:registry_url, image_name
    """
    s = repo_name.split("/", 1)
    if len(s) > 1:
        return s[0], s[1]
    return "", repo_name


def delete_from_registry(repo_name, tag):
    try:
        logging.info('repo_name = %s, tag = %s'%(repo_name, tag))
        registry_url, image_name = parse_repo(repo_name)
        #logger.info("delete image {0} version {1} registry_url {2}".format(image_name, tag, registry_url))
        # print "registry_url:", registry_url
        # print "image_name:", image_name
        registry_client = DockerRegistryClient("".join([regisry_protocol, registry_url]), verify_ssl=False,
                                               api_version=2)
        repo = registry_client.repository(image_name)
        manifest, digest = repo.manifest(tag)
        #logger.info("delete image digest from registry {0}".format(digest))
        # print "image digest:", digest
        repo.delete_manifest(digest)
    except HTTPError as e:
        logging.error(e)
        if e.response.status_code == 404:
            pass
        else:
           raise
    except Exception as e:
        # print traceback.format_exc()
        logging.error(e)
        raise


def get_app_slave(image_url):
    logging.info('image_url = %s'%image_url)
    slave_hosts = []
    apps = dbapi.get_app_slaves(image_url)
    for _, _, app_info in apps:
        if app_info:
            slave_hosts.append(app_info.slave_ip)

    logging.info('return %s'%slave_hosts)
    return slave_hosts


def update_image_info(repo_name, version=None):
    logging.info('repo_name = %s'%repo_name)
    try:
        dbapi.update_image_version_deleted(repo_name, version)
        if version:
            dbapi.update_image_version_count(repo_name)
            if not dbapi.get_image_versions(repo_name):
                dbapi.update_image_deleted(repo_name)
            dbapi.update_image_latest_version(repo_name)
        else:
            dbapi.update_image_deleted(repo_name)
    except Exception as e:
        logging.error(e)
        raise


def image_used(repo_name, version=None):
    """
    check image is used
    :param repo_name:
    :param version:
    :return:True or False
    """
    used = False
    if version:
        image_url = "".join([repo_name, ":", version])
        if dbapi.get_app_by_image(image_url):
            used = True
    else:
        images = dbapi.get_image_versions(repo_name)
        for image in images:
            version = image.version
            image_url = "".join([repo_name, ":", version])
            if dbapi.get_app_by_image(image_url):
                used = True
                break
    return used

