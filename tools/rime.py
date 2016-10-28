#!/usr/bin/env python3
#
# Copyright (C) librime developers
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from ctypes import *
from time import time
import sys, os

ENC = sys.getfilesystemencoding()
RIME = "Rime"
_librime = None
if sys.platform == "win32": # Windows
    import os.path
    # find in current dir first
    dll_path = os.path.join(os.path.dirname(__file__), "rime.dll")
    if not os.path.exists(dll_path):
        dll_path = "rime.dll" # search in system path
    _librime = CDLL(dll_path)
else: # UNIX-like systems
    _librime = CDLL('librime.so')

RimeSessionId = POINTER(c_uint)
RimeNotificationHandler = CFUNCTYPE(None, c_void_p, RimeSessionId, c_char_p, c_char_p)
Bool = c_int
RIME_MAX_NUM_CANDIDATES = 10
CHAR_SIZE = 100

class RIME_STRUCT(Structure):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_size = sizeof(self) - sizeof(c_int)

    def has_member(self, member):
        return hasattr(self, member)

    def __del__(self):
        try:
            memset(self, 0, sizeof(self))
        except:
            pass
        finally:
            del self

class RimeTraits(RIME_STRUCT):
    _fields_ = [
        ("data_size", c_int),
        ("shared_data_dir", c_char_p),
        ("user_data_dir", c_char_p),
        ("distribution_name", c_char_p),
        ("distribution_code_name", c_char_p),
        ("distribution_version", c_char_p),
        ("app_name", c_char_p),
        ("modules", POINTER(c_char_p))]

class RimeComposition(Structure):
    _fields_ = [
        ("length", c_int),
        ("cursor_pos", c_int),
        ("sel_start", c_int),
        ("sel_end", c_int),
        ("preedit", c_char_p)]

class RimeCandidate(Structure):
    _fields_ = [
        ("text", c_char_p),
        ("comment", c_char_p),
        ("reserved", c_void_p)]

class RimeMenu(Structure):
    _fields_ = [
        ("page_size", c_int),
        ("page_no", c_int),
        ("is_last_page", Bool),
        ("highlighted_candidate_index", c_int),
        ("num_candidates", c_int),
        ("candidates", POINTER(RimeCandidate)),
        ("select_keys", c_char_p)]

class RimeCommit(RIME_STRUCT):
    _fields_ = [
        ("data_size", c_int),
        ("text", c_char_p)]

class RimeContext(RIME_STRUCT):
    _fields_ = [
        ("data_size", c_int),
        ("composition", RimeComposition),
        ("menu", RimeMenu),
        ("commit_text_preview", c_char_p),
        ("select_labels", POINTER(c_char_p))
        ]

class RimeStatus(RIME_STRUCT):
    _fields_ = [
        ("data_size", c_int),
        ("schema_id", c_char_p),
        ("schema_name", c_char_p),
        ("is_disabled", Bool),
        ("is_composing", Bool),
        ("is_ascii_mode", Bool),
        ("is_full_shape", Bool),
        ("is_simplified", Bool),
        ("is_traditional", Bool),
        ("is_ascii_punct", Bool),
        ]

class RimeCandidateListIterator(Structure):
    _fields_ = [
        ("ptr", c_void_p),
        ("index", c_int),
        ("candidate", RimeCandidate)]

class RimeConfig(Structure):
    _fields_ = [("ptr", c_void_p)]

class RimeConfigIterator(Structure):
    _fields_ = [
        ("list", c_void_p),
        ("map", c_void_p),
        ("index", c_int),
        ("key", c_char_p),
        ("path", c_char_p)]

class RimeSchemaListItem(Structure):
    _fields_ = [
        ("schema_id", c_char_p),
        ("name", c_char_p),
        ("reserved", c_void_p)]

class RimeSchemaList(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("list", POINTER(RimeSchemaListItem))]

class RimeCustomApi(RIME_STRUCT):
    _fields_ = [("data_size", c_int)]

class RimeModule(RIME_STRUCT):
    _fields_ = [("data_size", c_int),
        ("module_name", c_char_p),
        ("initialize", c_void_p),
        ("finalize", c_void_p),
        ("get_api", CFUNCTYPE(POINTER(RimeCustomApi)))
        ]

_librime.RimeCreateSession.restype = RimeSessionId
_librime.RimeConfigGetCString.restype = c_char_p
_librime.RimeConfigListSize.restype = c_size_t
_librime.RimeGetSharedDataDir.restype=c_char_p
_librime.RimeGetUserDataDir.restype=c_char_p
_librime.RimeGetSyncDir.restype=c_char_p
_librime.RimeGetUserId.restype=c_char_p
_librime.RimeFindModule.restype = POINTER(RimeModule)

class RimeApi(RIME_STRUCT):
    _fields_ = [("data_size", c_int),
        ("setup", CFUNCTYPE(None, POINTER(RimeTraits))),
        ("set_notification_handler", CFUNCTYPE(None, RimeNotificationHandler, c_void_p)),
        ("initialize", CFUNCTYPE(None, POINTER(RimeTraits))),
        ("finalize", CFUNCTYPE(None)),
        ("start_maintenance", CFUNCTYPE(Bool, Bool)),
        ("is_maintenance_mode", CFUNCTYPE(Bool)),
        ("join_maintenance_thread", CFUNCTYPE(None)),
        ("deployer_initialize", CFUNCTYPE(None, POINTER(RimeTraits))),
        ("prebuild", CFUNCTYPE(Bool)),
        ("deploy", CFUNCTYPE(Bool)),
        ("deploy_schema", CFUNCTYPE(Bool, c_char_p)),
        ("deploy_config_file", CFUNCTYPE(Bool, c_char_p, c_char_p)),
        ("sync_user_data", CFUNCTYPE(Bool)),
        ("create_session", CFUNCTYPE(RimeSessionId)),
        ("find_session", CFUNCTYPE(Bool, RimeSessionId)),
        ("destroy_session", CFUNCTYPE(Bool, RimeSessionId)),
        ("cleanup_stale_sessions", CFUNCTYPE(None)),
        ("cleanup_all_sessions", CFUNCTYPE(None)),
        ("process_key", CFUNCTYPE(Bool, RimeSessionId, c_int, c_int)),
        ("commit_composition", CFUNCTYPE(Bool, RimeSessionId)),
        ("clear_composition", CFUNCTYPE(None, RimeSessionId)),
        ("get_commit", CFUNCTYPE(Bool, RimeSessionId, POINTER(RimeCommit))),
        ("free_commit", CFUNCTYPE(Bool, POINTER(RimeCommit))),
        ("get_context", CFUNCTYPE(Bool, RimeSessionId, POINTER(RimeContext))),
        ("free_context", CFUNCTYPE(Bool, POINTER(RimeContext))),
        ("get_status", CFUNCTYPE(Bool, RimeSessionId, POINTER(RimeStatus))),
        ("free_status", CFUNCTYPE(Bool, POINTER(RimeStatus))),
        ("set_option", CFUNCTYPE(None, RimeSessionId, c_char_p, Bool)),
        ("get_option", CFUNCTYPE(Bool, RimeSessionId, c_char_p)),
        ("set_property", CFUNCTYPE(None, RimeSessionId, c_char_p, c_char_p)),
        ("get_property", CFUNCTYPE(Bool, RimeSessionId, c_char_p, c_char_p, c_size_t)),
        ("get_schema_list", CFUNCTYPE(Bool, POINTER(RimeSchemaList))),
        ("free_schema_list", CFUNCTYPE(None, POINTER(RimeSchemaList))),
        ("get_current_schema", CFUNCTYPE(Bool, RimeSessionId, c_char_p, c_size_t)),
        ("select_schema", CFUNCTYPE(Bool, RimeSessionId, c_char_p)),
        ("schema_open", CFUNCTYPE(Bool, c_char_p, POINTER(RimeConfig))),
        ("config_open", CFUNCTYPE(Bool, c_char_p, POINTER(RimeConfig))),
        ("config_close", CFUNCTYPE(Bool, POINTER(RimeConfig))),
        ("config_get_bool", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, POINTER(Bool))),
        ("config_get_int", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, POINTER(c_int))),
        ("config_get_double", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, POINTER(c_double))),
        ("config_get_string", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, c_char_p, c_size_t)),
        ("config_get_cstring", CFUNCTYPE(c_char_p, POINTER(RimeConfig), c_char_p)),
        ("config_update_signature", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p)),
        ("config_begin_map", CFUNCTYPE(Bool, POINTER(RimeConfigIterator), POINTER(RimeConfig), c_char_p)),
        ("config_next", CFUNCTYPE(Bool, POINTER(RimeConfigIterator))),
        ("config_end", CFUNCTYPE(None, POINTER(RimeConfigIterator))),
        ("simulate_key_sequence", CFUNCTYPE(Bool, RimeSessionId, c_char_p)),
        ("register_module", CFUNCTYPE(Bool, POINTER(RimeModule))),
        ("find_module", CFUNCTYPE(POINTER(RimeModule), c_char_p)),
        ("run_task", CFUNCTYPE(Bool, c_char_p)),
        ("get_shared_data_dir", CFUNCTYPE(c_char_p)),
        ("get_user_data_dir", CFUNCTYPE(c_char_p)),
        ("get_sync_dir", CFUNCTYPE(c_char_p)),
        ("get_user_id", CFUNCTYPE(c_char_p)),
        ("get_user_data_sync_dir", CFUNCTYPE(None, c_char_p, c_size_t)),
        ("config_init", CFUNCTYPE(Bool, POINTER(RimeConfig))),
        ("config_load_string", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p)),
        ("config_set_bool", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, Bool)),
        ("config_set_int", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, c_int)),
        ("config_set_double", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, c_double)),
        ("config_set_string", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, c_char_p)),
        ("config_get_item", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, POINTER(RimeConfig))),
        ("config_set_item", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p, POINTER(RimeConfig))),
        ("config_clear", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p)),
        ("config_create_list", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p)),
        ("config_create_map", CFUNCTYPE(Bool, POINTER(RimeConfig), c_char_p)),
        ("config_list_size", CFUNCTYPE(c_size_t, POINTER(RimeConfig), c_char_p)),
        ("config_begin_list", CFUNCTYPE(Bool, POINTER(RimeConfigIterator), POINTER(RimeConfig), c_char_p)),
        ("get_input", CFUNCTYPE(c_char_p, RimeSessionId)),
        ("get_caret_pos", CFUNCTYPE(c_size_t, RimeSessionId)),
        ("select_candidate", CFUNCTYPE(Bool, RimeSessionId, c_size_t)),
        ("get_version", CFUNCTYPE(c_char_p)),
        ("set_caret_pos", CFUNCTYPE(None, RimeSessionId, c_size_t)),
        ("select_candidate_on_current_page", CFUNCTYPE(Bool, RimeSessionId, c_size_t)),
        ("candidate_list_begin", CFUNCTYPE(Bool, RimeSessionId, POINTER(RimeCandidateListIterator))),
        ("candidate_list_next", CFUNCTYPE(Bool, POINTER(RimeCandidateListIterator))),
        ("candidate_list_end", CFUNCTYPE(None, POINTER(RimeCandidateListIterator))),
        ]

_librime.rime_get_api.restype = POINTER(RimeApi)

rime = _librime.rime_get_api().contents

def rimeNotificationHandler(context_object, session_id, message_type, message_value):
    print(context_object, session_id.contents if session_id else 0, message_type, message_value)

def rimeInit(datadir="data", userdir="data", fullcheck=True, appname="python", appver="0.01"):
    traits = RimeTraits(
        shared_data_dir=c_char_p(datadir.encode(ENC)),
        user_data_dir=c_char_p(userdir.encode(ENC)),
        distribution_name=c_char_p(RIME.encode("UTF-8")),
        distribution_code_name=c_char_p(appname.encode("UTF-8")),
        distribution_version=c_char_p(appver.encode("UTF-8")),
        app_name=c_char_p(("%s.%s"%(RIME, appname)).encode("UTF-8"))
        )
    rime.setup(traits)
    #cb = RimeNotificationHandler(rimeNotificationHandler)
    #rime.set_notification_handler(cb, byref(rime))
    rime.initialize(None)
    if rime.start_maintenance(fullcheck):
        rime.join_maintenance_thread()

def rimeGetString(config, name):
    cstring = rime.config_get_cstring(config, name.encode("UTF-8"))
    return cstring.decode("UTF-8") if cstring else ""

def rimeSelectSchema(session_id, schema_id):
    rime.select_schema(session_id, schema_id)
    user_config = RimeConfig()
    if rime.config_open(b'user', user_config):
        rime.config_set_string(user_config, b'var/previously_selected_schema', schema_id)
        rime.config_set_int(user_config, b'var/schema_access_time/' + schema_id, c_int(int(time())))
        rime.config_close(user_config)

def processKey(session_id, keycode, mask):
    print("process_key", keycode, "ret", rime.process_key(session_id, keycode, mask))
    status = RimeStatus()
    if rime.get_status(session_id, status):
        print("is_composing",  status.is_composing)
        print("is_ascii_mode",  status.is_ascii_mode)
        print("current_schema", status.schema_name.decode("UTF-8"))
        rime.free_status(status)

    commit = RimeCommit()
    if rime.get_commit(session_id, commit):
        print("commit",commit.text.decode("UTF-8"))
        rime.free_commit(commit)

    context = RimeContext()
    if not rime.get_context(session_id, context) or context.composition.length == 0:
        rime.free_context(context)
        exit

    if context.commit_text_preview:
        commit_text_preview = context.commit_text_preview.decode("UTF-8")
        print("commit_text_preview",commit_text_preview)

    if context.composition.length:
        print("preedit", context.composition.preedit.decode("UTF-8"),
              "cursor_pos", context.composition.cursor_pos,
              "sel_start", context.composition.sel_start,
              "sel_end", context.composition.sel_end)

    if context.menu.page_size:
        print("page_size",context.menu.page_size)
        select_keys = b''
        if context.select_labels:
            for i in range(context.menu.page_size):
                select_keys += context.select_labels[i]
        elif context.menu.select_keys:
            select_keys = context.menu.select_keys
        if select_keys:
            print("select_keys",select_keys.decode("UTF-8"))

    if context.menu.num_candidates:
        print("num_candidates", context.menu.num_candidates)
        candidates = []
        for i in range(context.menu.num_candidates):
            cand = context.menu.candidates[i]
            s = cand.text
            if cand.comment:
                s += b' ' + cand.comment
            candidates.append(s.decode("UTF-8"))
        print(candidates)
    rime.free_context(context)

def processText(session_id, text, start = 0, count = sys.maxsize):
    rime.simulate_key_sequence(session_id, c_char_p(text.encode("UTF-8")))
    candidate_list = RimeCandidateListIterator()
    texts =[]
    if rime.candidate_list_begin(session_id, candidate_list):
        index = 0
        end = start + count
        while rime.candidate_list_next(candidate_list):
            if start <= index < end:
                texts.append(candidate_list.candidate.text.decode("UTF-8"))
            elif index >= end:
                break
            index += 1
        rime.candidate_list_end(candidate_list)
    return texts

def printTexts(texts, output_format):
    if output_format == "elisp":
        print('("%s")'%('" "'.join(texts)))
    elif output_format == "json":
        import json
        print(json.dumps(texts))
    else:
        print(texts)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("%s code [python|json|elisp] [start=0] [count=%d]" % (sys.argv[0], sys.maxsize))
        exit(0)
    rimeInit(datadir="/usr/share/rime-data/", userdir=os.path.expanduser("~/.config/ibus/rime/"), fullcheck=False, appname="ibus-rime", appver="1.2")
    session_id = rime.create_session()
    start = int(sys.argv[3]) if len(sys.argv) >= 4 and sys.argv[3].isnumeric() else 0
    count = int(sys.argv[4]) if len(sys.argv) >= 5 and sys.argv[4].isnumeric() else sys.maxsize
    texts = processText(session_id, sys.argv[1], start, count)
    output_format = sys.argv[2] if len(sys.argv) >= 3 else ""
    printTexts(texts, output_format)
    rime.destroy_session(session_id)
    rime.finalize()
