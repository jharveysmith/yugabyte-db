/*--------------------------------------------------------------------------------------------------
 *
 * yb_virtual_wal_client_typedefs.h
 *
 * Copyright (c) YugaByte, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied.  See the License for the specific language governing permissions and limitations
 * under the License.
 *
 * src/include/replication/yb_virtual_wal_client_typedefs.h
 *
 *--------------------------------------------------------------------------------------------------
 */

#ifndef YB_VIRTUAL_WAL_CLIENT_TYPEDEFS_H
#define YB_VIRTUAL_WAL_CLIENT_TYPEDEFS_H

#include "access/xlogdefs.h"
#include "c.h"
#include "nodes/pg_list.h"
#include "yb/yql/pggate/ybc_pg_typedefs.h"

typedef struct PgVirtualWalRecord
{
	YBCPgRowMessage *data;
	XLogRecPtr lsn;
	TransactionId xid;
	Oid table_oid;
} YBCPgVirtualWalRecord;

#endif