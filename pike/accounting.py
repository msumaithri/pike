#
# Copyright (c) 2016, Dell Technologies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Module Name:
#
#        accounting.py
#
# Abstract:
#
#        Accounting plugin for smb2
#
# Authors: Masen Furer (masen.furer@dell.com)
#

import smb2

def smb2_accounting(nb_frame):
    smb_frame = nb_frame[0]
    if isinstance(smb_frame, smb2.NegotiateRequest) or isinstance(smb_frame, smb2.NegotiateResponse):
        return
    conn = nb_frame.conn
    accounting_data = {
            'proc': int(smb_frame.command),
            'proc_name': str(smb_frame.command),
            'client': conn.local_addr[0],
            'size': len(nb_frame.buf),
            'type': "RESP" if smb_frame.flags & smb2.SMB2_FLAGS_SERVER_TO_REDIR else "CALL"
    }
    session = conn.session(smb_frame.session_id)
    if session is not None:
        accounting_data['user'] = session.user
        tree = session.tree(smb_frame.tree_id)
        if tree is not None:
            accounting_data['share'] = session.tree(smb_frame.tree_id).path.rpartition("\\")[-1]
    print(accounting_data)
