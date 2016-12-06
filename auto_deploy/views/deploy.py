# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import shlex

from flask import Blueprint, jsonify
from flask.views import MethodView

from ..core import logger
from ..models import DeployScript


bp = Blueprint('deploy', __name__)


class DeployView(MethodView):
    def get(self, alias):
        return self.post(alias)

    def post(self, alias):
        # can use request.get_json()
        logger.info('exec ' + alias)
        ds = DeployScript.get_by_alias(alias)
        command = shlex.split(ds.command)
        with Popen(command, cwd=ds.cwd,
                   stdin=PIPE, stdout=PIPE,
                   universal_newlines=True) as proc:
            returncode = proc.wait()
            stdout, stderr = proc.communicate()
            msg = []
            msg.append('alias: ' + alias)
            msg.append('command: ' + str(command))
            msg.append('cwd: ' + ds.cwd)
            msg.append('returncode: ' + str(returncode))
            msg.append('stdout: ' + str(stdout))
            msg.append('stderr: ' + str(stderr))
            logger.info('\n'.join(msg))
            return jsonify(
                returncode=returncode,
                stdout=stdout,
                stderr=stderr
            )


bp.add_url_rule('/deploy/<alias>', view_func=DeployView.as_view('deploy'))
