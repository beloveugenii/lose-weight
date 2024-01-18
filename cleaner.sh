#!/bin/bash

echo 'delete from current_user' | sqlite3 db.sqlite
rm -rf __pycache__/
rm -rf libs/__pycache__/

