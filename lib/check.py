#!/usr/bin/env python

# check utils used pexpect
# by cshi
# 4.Jan.2015

import pexpect
import logging
import re


# =================== basic =====================
def check_no_input(cmd, check):
    logger = logging.getLogger('check no input')
    child = pexpect.spawn(cmd, timeout=60)
    index = child.expect([check, pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


# =================== init   =====================
def check_init_server(cmd, check, password):
    logger = logging.getLogger('check_init_server')
    logger.info(cmd)
    child = pexpect.spawn(cmd)
    index = child.expect([check, 'Password', 'Generate a token now', pexpect.TIMEOUT, pexpect.EOF])
    if index == 0:
        logger.info('< ' + cmd + ' > [pass]')
    elif index == 1:
        child.sendline(password)
        index = child.expect([check, 'Generate a token now'])
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
        elif index == 1:
            child.sendline('yes')
            index = child.expect(check)
            if index == 0:
                logger.info('< ' + cmd + ' > [pass]')
            else:
                logger.info('< ' + cmd + ' > [fail]')
    elif index == 2:
        child.sendline('yes')
        index = child.expect(check)
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
    elif index == 3:
        logger.info('< ' + cmd + ' > [Timeout]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


# =================== server =====================
def check_add_server(cmd, account, password):
    logger = logging.getLogger('check add server')
    child = pexpect.spawn(cmd, timeout=60)
    index = child.expect('Login to')
    if index == 0:
        child.sendline(account)
        index = child.expect('Password')
        if index == 0:
            child.sendline(password)
            index = child.expect('Generate a token')
            if index == 0:
                child.sendline('yes')
                index = child.expect('Saving server configuration to')
                if index == 0:
                    logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + '> [fail]')


def check_change_server(cmd, password):
    logger = logging.getLogger('check change server')
    child = pexpect.spawn(cmd, timeout=60)
    index = child.expect('Password')
    if index == 0:
        child.sendline(password)
        index = child.expect('Now using')
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


# ================= app ==========================
def check_create_app(cmd):
    logger = logging.getLogger('check create app')
    child = pexpect.spawn(cmd)
    index = child.expect(['Are you sure you want to continue connecting', 'Your application \'(\w+)\' is now available'], timeout=None)
    if index == 0:
        child.sendline('yes')
        index = child.expect('Your application \'(\w+)\' is now available')
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
    elif index == 1:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


def compute_app_count():
    logger = logging.getLogger('compute app count')
    child = pexpect.spawn('rhc apps')
    child.expect(pexpect.EOF)
    apps = re.findall(r'.+?(?=\s@)', child.before)
    logger.info('app counts : ' + str(apps.__len__()))
    return apps.__len__()


def check_unovercmd_app(cmd, check):
    logger = logging.getLogger('check unovercmd app')
    child = pexpect.spawn(cmd, timeout=20)
    child.expect(pexpect.TIMEOUT)
    log = re.findall(check, child.before)
    if log.__len__() != 0:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.info('< ' + cmd + ' > [fail]')


def recovery_account_after_expired(passwd):
    logger = logging.getLogger('recovery account after expired')
    child = pexpect.spawn('rhc apps')
    index = child.expect(['Password', pexpect.TIMEOUT])
    if index == 0:
        child.sendline(passwd)
        logger.info('recovery account after expired ... succeed')


def get_commit_id():
    logger = logging.getLogger('get commit id')
    child = pexpect.spawn('rhc deployment list -a app')
    child.expect(pexpect.EOF)
    logger.info(child.before)
    logger.info('-------------------')
    commid = re.findall(r'(\w+){8}$', child.before)
    logger.info('commid id : ' + commid[0])
    return commid[0]


def get_haproxy_time(cmd):
    logger = logging.getLogger('get haproxy time')
    child = pexpect.spawn(cmd)
    child.expect(pexpect.EOF)
    haproxy = re.findall(r'haproxy', child.before)
    logger.info('haproxy : ' + str(haproxy.__len__()))
    return haproxy.__len__()


# ================= cartridge ==========================
def check_rhc_caritridge(cmd, check):
    logger = logging.getLogger('check rhc caritridge')
    child = pexpect.spawn(cmd)
    index = child.expect(pexpect.TIMEOUT, timeout=30)
    if index == 0:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


def get_additional_storage(cmd):
    logger = logging.getLogger('get additional storage')
    child = pexpect.spawn(cmd)
    child.expect(pexpect.EOF)
    storage = re.findall(r'\d', child.before)
    logger.info('additional storage : ' + storage[0])
    return int(storage[0])


# ================= env ==============================
def check_remove_env(cmd):
    logger = logging.getLogger('check remove env')
    child = pexpect.spawn(cmd)
    index = child.expect('Are you sure you wish to remove the environment variable\(s\)', timeout=60)
    if index == 0:
        child.sendline('yes')
        index = child.expect('Removing environment variable\(s\).*done')
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


# ================= team =============================
def check_leave_team(cmd, password1, password2):
    logger = logging.getLogger('check leave team')
    child = pexpect.spawn(cmd)
    index = child.expect(['Password', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        child.sendline(password2)
        index = child.expect(['Leaving team.*done', pexpect.TIMEOUT])
        if index == 0:
            logger.info('< ' + cmd + ' > [pass]')
    elif index == 1:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')
    child.sendline('rhc account')
    index = child.expect(['Password', pexpect.EOF])
    if index == 0:
        child.sendline(password1)


# ================ authorization =====================
def check_rhc_authorization(cmd):
    logger = logging.getLogger('check rhc authorization')
    child = pexpect.spawn(cmd)
    index = child.expect(pexpect.EOF)
    if index == 0:
        token = re.findall(r'[\w+]{64}', child.before)
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')
    return token[0]


def check_authorization_list(cmd):
    logger = logging.getLogger('check authorization list')
    child = pexpect.spawn(cmd)
    index = child.expect(pexpect.EOF)
    authorizations = re.findall(r'abcd', child.before)
    logger.info('authorization counts : ' + str(authorizations.__len__()))
    if authorizations.__len__() == 3:
        logger.info('< ' + cmd + ' > [pass]')
    else:
        logger.error('< ' + cmd + ' > [fail]')


def check_authorization_list_after_delete_all(password):
    logger = logging.getLogger('check authorization list after delete all')
    child = pexpect.spawn('rhc authorization list')
    index = child.expect('Password')
    if index == 0:
        child.sendline(password)
        logger.info('< rhc authorization list after delete all > [fail]')
    else:
        logger.error('< rhc authorization list after delete all > [fail]')