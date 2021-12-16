#!/bin/bash
cp ftp_upload.conf /etc/supervisor/conf.d/ftp_upload.conf
supervisorctl reread
supervisorctl update
supervisorctl start ftp_upload
supervisorctl start nat
