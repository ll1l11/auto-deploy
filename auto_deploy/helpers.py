# -*- coding: utf-8 -*-
import pkgutil
import importlib
from datetime import datetime, date, time
from numbers import Number
from decimal import Decimal

from flask import Blueprint


def register_blueprints(app, module_prefix, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param module_prefix: a string on the front of every module name
    :param package_path: a path to look for modules in
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules([package_path], module_prefix):
        m = importlib.import_module(name)
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class JSONSerializer(object):
    _json_include = None
    _json_exclude = None
    _json_simple = None

    def get_field_names(self):
        # for p in self.__mapper__.iterate_properties:
        #     yield p.key
        # _keys = self.__mapper__.c.keys()
        return [x.name for x in self.__table__.columns]

    def _get_serial_value(self, key):
        """JSON serializer for objects not serializable by default json code"""
        val = getattr(self, key)
        if val is None or isinstance(val, (str, int)):
            pass
        elif isinstance(val, Decimal):
            return float(val)
        elif isinstance(val, Number):
            pass
        elif isinstance(val, datetime):
            val = val.isoformat(' ')
        elif isinstance(val, (date, time)):
            val = val.isoformat()
        elif isinstance(val, JSONSerializer):
            val = val.to_json_simple()
        elif isinstance(val, list):
            l = []
            for item in val:
                l.append(self._serial_value(item))
            val = l

        return val

    def _get_json_keys(self, include, exclude, only):
        if only:
            return only

        exclude_set = {'password'}
        if self._json_exclude:
            exclude_set.update(self._json_exclude)
        if exclude:
            exclude_set.update(exclude)

        include_set = set()
        if self._json_include:
            include_set.update(self._json_include)
        if include:
            include_set.update(include)

        keys_set = set(self.get_field_names())
        keys_set.difference_update(exclude_set)
        keys_set.update(include_set)

        return keys_set

    def to_json(self, include=None, exclude=None, only=None):
        keys = self._get_json_keys(include, exclude, only)
        data = {key: self._get_serial_value(key) for key in keys}
        return data or None

    def to_json_simple(self):
        only = self._todict_simple_keys()
        if not only:
            only = set(x for x in self.get_field_names if x in {'id', 'name'})
        return self.to_json(only=only)
