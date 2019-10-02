#!/usr/bin/env python3

import os
import subprocess
import sys

#from nutils import get_temporary_file_name

__all__ = ["get_temporary_file_name", "exe_cmd"]

def get_temporary_file_name(dirn="/tmp"):
    import uuid
    return dirn + "/" + str(uuid.uuid4())

def exe_cmd(cmd, num_returns=0, echo=False):
    """Execute shell command

    Input args:
        cmd (str): shell command
        num_returns (int): number of returns (0, 1 or 3)
        echo (bool): whether echo the given command or not

    Returns:
        when num_returns=0:
        None

        when num_returns=1:
        sts (int): exit status

        when num_returns=3:
        sts (int): exit status
        out (str): output from the command
        err (str): error output from the command

    Notes:

        1) When the executed command fails, the function fails
           with num_returns=0. With num_returns=1 or 3, the function
           does not fail but simply return non-zero value as status.
    """

    if echo == True:
        print("Executing shell command:", cmd)
        print()

    if num_returns in [0, 1]:
        sts = subprocess.call(cmd, shell=True)

        if num_returns == 0 and sts != 0:
            sys.exit(sts)

        if num_returns == 0:
            return None

        return sts
        
    if num_returns == 3:
        out, err, sts = "", "", 0

        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
        except subprocess.CalledProcessError as exc:
            err = exc.output.decode("utf-8")
            sts = 1

        return sts, out, err
