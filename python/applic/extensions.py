# -*- coding: utf-8 -*-
"""Extensions module for the 'Main Angular application package'.
Each extension is initialized in the app factory located in applic/app.py."""
#
# Exception module for the 'Main Angular application package'.
# Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
from flask import Flask as BaseFlask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model

from applic.config import Config


class Flask( BaseFlask ):
    """Extended version of `Flask` that implements custom config class"""
    def make_config( self, instance_relative = False ):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path

        return Config( root_path, self.default_config )


class CRUDMixin( Model ):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update( self, commit = True, **kwargs ):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr( self, attr, value )

        return commit and self.save() or self

    def save( self, commit = True ):
        """Save the record."""
        db.session.add( self )
        if commit:
            db.session.commit()

        return self

    def delete( self, commit = True ):
        """Remove the record from the database."""
        db.session.delete( self )
        return commit and db.session.commit()


bcrypt  = Bcrypt()
db      = SQLAlchemy( model_class = CRUDMixin )
migrate = Migrate()
cache   = Cache()
cors    = CORS()
jwt     = JWTManager()

