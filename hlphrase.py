__module_name__ = 'hlphrase'
__module_description__ = 'highlights phrases instead of just single words'
__module_version__ = '1.0'

import hexchat, re

CONFFILE = hexchat.get_info('configdir')  + '/hlphrase.conf'
list=[]

hexchat.prnt('%(name)s, version %(version)s' % {'name': __module_name__,  'version': __module_version__})  

def read_list():
    try:
        conf = open(CONFFILE,'r')
    except:
        hexchat.prnt(CONFFILE + " currently doesn't exist, creating")
        return None
    lines = conf.readlines()
    for each in lines:
        list.append(re.sub(r'\n','',each))
    conf.close()


def save_list():
    conf = open(CONFFILE,'w')
    for phrase in list:
        conf.write(phrase + '\n')
    conf.close()


def check_msg(word, word_eol, userdata):
    for phrase in list:
        if phrase in word_eol[1].lower():
            hexchat.command("gui color 3")
            hexchat.emit_print( "Channel Msg Hilight", word[0], word[1] )
            return hexchat.EAT_ALL
    
    return hexchat.EAT_NONE


def add_hilight_phrase(word, word_eol, userdata):
    if len(word) <= 2:
        return list_hilight_phrase(word, word_eol, userdata)
    phrase = word_eol[2]
    if phrase not in list:
        list.append(phrase)
        hexchat.prnt('\x032* "%s" will be hilighted' % phrase)
    else:
        hexchat.prnt('\x032* "%s" is already being hilighted' % phrase)
    save_list()
    return hexchat.EAT_HEXCHAT


def list_hilight_phrase(word, word_eol, userdata):
    hexchat.command('query @hilight')
    tab = hexchat.find_context(channel='@hilight')
    tab.prnt('\x032Current hilight-phrase list: %d hilighted.' % len(list))
    for index, phrase in enumerate(list):
        tab.prnt('\x032 %s -- %s' % (index, phrase))
    tab.prnt('\x032* End of hilight-phrase list')
    return hexchat.EAT_HEXCHAT


def remove_hilight_phrase(word, word_eol, userdata):
    if len(word) <= 2:
        return list_hilight_phrase(word, word_eol, userdata)
    index = int(word[2])
    if index >= 0 and index < len(list):
        hexchat.prnt('\x032 "%s" has been removed from the hilight list' % list[index])
        del list[index]
    else:
        hexchat.prnt('\x032 %d is not a valid selection' % index)

    save_list()
    return hexchat.EAT_HEXCHAT

def help_list(word, word_eol, userdata):
    hexchat.command('query @hilight')
    tab = hexchat.find_context(channel='@hilight')
    tab.prnt('/hilight add <phrase> - add <phrase> to list of strings to highlist')
    tab.prnt('/hilight list - print current list of strings to highlight')
    tab.prnt('/hilight remove <index> - remove list item #<index> from list of strings to hightlist')
    tab.prnt('/hilight help - print this message')
    return hexchat.EAT_HEXCHAT


def choose(word, word_eol, userdata):
    if len(word) == 1:
        return help_list(word, word_eol, userdata)
    command = word[1]
    if command == "add": return add_hilight_phrase(word, word_eol, userdata)
    if command == "remove": return remove_hilight_phrase(word, word_eol, userdata)
    if command == "list": return list_hilight_phrase(word, word_eol, userdata)
    if command == "help": return help_list(word, word_eol, userdata)

    hexchat.prnt("unknown option: %s, use '/hilight help' for help" % command)

    return hexchat.EAT_HEXCHAT


read_list()
hexchat.hook_command("hilight", choose)
hexchat.hook_print("Channel Message", check_msg)
