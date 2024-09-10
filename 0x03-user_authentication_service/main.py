#!/usr/bin/env python3
""" Main 0x03-user_authentication_service """

from user import User

print('table_name:', User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))
