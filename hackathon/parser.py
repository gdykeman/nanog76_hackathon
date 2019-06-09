#!/usr/bin/env python

import json
import sys

def ParseUpdate( update ):
    if 'announce' in update:
        x = update[ 'announce' ][ 'bgp-ls bgp-ls' ]
        for ip in x:
            r = x[ ip ]
            for announce in r:
                #sys.stderr.write( "DEBUG:\n" + json.dumps( announce ) + "\n" );
                announce[ 't3-type' ] = 'announce'
                if 1 == announce[ 'ls-nlri-type' ]:
                    HandleAnnounceNode( announce )
                    continue
                elif 2 == announce[ 'ls-nlri-type' ]:
                    HandleAnnounceLink( announce )
                    continue
                else:
                    sys.stderr.write( "UNKNOWN ANNOUNCE!!:\n"
                            + json.dumps( update ) + "\n\n" )

    elif 'withdraw' in update:
        x = update[ 'withdraw' ][ 'bgp-ls bgp-ls' ]
        for withdraw in update[ 'withdraw' ][ 'bgp-ls bgp-ls' ]:
            withdraw[ 't3-type' ] = 'withdraw'
            if 1 == withdraw[ 'ls-nlri-type' ]:
                HandleWithdrawNode( withdraw )
                continue
            elif 2 == withdraw[ 'ls-nlri-type' ]:
                HandleWithdrawLink( withdraw )
                continue
            else:
                sys.stderr.write( "UNKNOWN WITHDRAW!!:\n"
                        + json.dumps( update ) + "\n\n" )

    else:
        sys.stderr.write( "UNKNOWN!!:\n" + json.dumps( update ) + "\n\n" )


def HandleAnnounceNode( announce ):
    x = {
        'type': 'announce',
        'router': announce[ 'node-descriptors' ][ 'router-id' ],
    }
    HandleAnnounceNodeCooked( x )

def HandleAnnounceNodeCooked( announce ):
    #sys.stderr.write( "Announce Node:\n" + json.dumps( announce ) + "\n\n" )
    return

def HandleAnnounceLink( announce ):
    x = {
        'type': 'announce',
        'router-a': announce[ 'local-node-descriptors' ][ 'router-id' ],
        'ip-a': announce[ 'interface-address' ][ 'interface-address' ],
        'router-b': announce[ 'remote-node-descriptors' ][ 'router-id' ],
        'ip-b': announce[ 'neighbor-address' ][ 'neighbor-address' ],
    }
    HandleAnnounceLinkCooked( x )

def HandleAnnounceLinkCooked( announce ):
    sys.stderr.write( "Announce Link:\n" + json.dumps( announce ) + "\n\n" )
    return

def HandleWithdrawNode( withdraw ):
    x = {
        'type': 'withdraw',
        'router': withdraw[ 'node-descriptors' ][ 'router-id' ],
    }
    HandleWithdrawNodeCooked( x )

def HandleWithdrawNodeCooked( withdraw ):
    sys.stderr.write( "Withdraw Node:\n" + json.dumps( withdraw ) + "\n\n" )
    return

def HandleWithdrawLink( withdraw ):
    x = {
        'type': 'withdraw',
        'router-a': withdraw[ 'local-node-descriptors' ][ 'router-id' ],
        'ip-a': withdraw[ 'interface-address' ][ 'interface-address' ],
        'router-b': withdraw[ 'remote-node-descriptors' ][ 'router-id' ],
        'ip-b': withdraw[ 'neighbor-address' ][ 'neighbor-address' ],
    }
    HandleWithdrawLinkCooked( x )

def HandleWithdrawLinkCooked( withdraw ):
    sys.stderr.write( "Withdraw Link:\n" + json.dumps( withdraw ) + "\n\n" )
    return

for st in sys.stdin:
    st = st.strip()
    if "" == st:
        continue
    x = json.loads( st )
    if 'neighbor' in x:
        x = x[ 'neighbor' ]
        if 'message' in x:
            x = x[ 'message' ]
            if 'update' in x:
                x = x[ 'update' ]
                ParseUpdate( x )
                continue;
    sys.stderr.write( "Didn't parse this:\n" + json.dumps( x ) + "\n" );