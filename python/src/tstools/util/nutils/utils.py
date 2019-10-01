
import os

from . import exe_cmd, watch, msg_exc

__all__ = ["close_Z", "len_iter", "list_map",
           "open_Z", "read_file", "sort_by_list"]
__all__.extend(["DirectAccessFile", "nFTP", "Struct"])
__all__.extend(["gen_file_header", "get_url", "wget"])


class DirectAccessFile:
    __slots__ = ["fl", "fn", "key"]

    def __init__(self, fn):
        import shelve

        self.fn = os.path.abspath(fn)
        self.fl = shelve.open(fn)

    def read(self, rec):
        key = self._get_key(rec)
        if key in self.fl:
            return self.fl[key]
        else:
            msg_exc("Record %d does not exist" % (rec))

    def write(self, rec, data):
        key = self._get_key(rec)
        self.fl[key] = data

    def _get_key(self, rec):
        return "key%d" % (rec)

    def delete(self):
        self.fl.close()
        os.remove(self.fn)

    def get_file_name(self):
        return self.fn


def sort_by_list(inlist, bylist):
    assert len(inlist) == len(bylist)

    tmpl = list(zip(bylist, inlist))
    tmpl.sort()
    ret = [inl for _, inl in tmpl]

    return ret


class nFTP:
    def __init__(self):
        self.ftp = None

    def login(self, host, user="", passwd="", timeout=10):
        from ftplib import FTP
        self.ftp = FTP(host, user, passwd, timeout=timeout)
        self.ftp.login()

    def cd(self, target):
        self.ftp.cwd(target)

    def ls(self, path="."):
        ret = self.ftp.nlst(path)
        return ret

    def get(self, filename):
        self.ftp.retrbinary("RETR %s" % (filename), open(filename, "wb").write)

    def quit(self):
        self.ftp.quit()


def list_map(func, inpL):
    return list(map(func, inpL))


def len_iter(iiter):
    return sum(1 for _ in iiter)


def open_Z(fn):
    from nutils import exe_cmd

    tfn = get_temporary_file_name()
    exe_cmd("gunzip -c %s > %s" % (fn, tfn))
    return tfn


def close_Z(tfn):
    from nutils import exe_cmd

    exe_cmd("rm %s" % (tfn))
    return


def gen_file_header(cmt, labels):
    line = cmt
    for ind in range(0, len(labels), 2):
        fmt = "%%%ss" % (labels[ind+1])
        line += fmt % (labels[ind])

    return line


class Struct:
    def __init__(self):
        self.attr_list = []

    def add_attr(self, var, default):
        self.__setattr__(var, default)
        self.attr_list.append(var)

    def get_attr(self, var):
        return self.__getattribute__(var)

    def get_attr_list(self):
        return self.attr_list[:]

    def set_attr(self, var, value):
        assert var in self.attr_list
        self.__setattr__(var, value)


def read_file(fn, specL, cmt="#"):
    """read table ascii file

    Inputs:
        - fn -- function name
        - specL -- column specification
        - cmt -- comment line character

    Outputs:
        - data -- data in Struct data structure

    Example:
        - Format of column specification is "{column number}|{column tag}|{data type}"
          For example, "0|mjd|f" means read the first column as floating point with
          tag "mjd". Use data.mjd to access this data.

          ex. read_file(file_name, "0:mjd:f, 1:stn:s")
    """

    if type(specL) == type(""):
        tmpL = []
        for spec in specL.split(","):
            spec = spec.replace(":", "|")
            tmpL.append(spec)
        specL = tmpL

    if type(specL[0]) == type(""):
        tmpL = []
        for spec in specL:
            tmp = spec.split("|")
            tmpL.append((int(tmp[0]), tmp[1], tmp[2]))
        specL = tmpL

    if len(specL[0]) == 2:
        tmpL = []
        for spec in specL:
            tmp = spec[1].split("|")
            tmpL.append((spec[0], tmp[0], tmp[1]))
        specL = tmpL

    nameL = [name for _, name, _ in specL]

    class Data:
        pass

    data = Struct()
    for name in nameL:
        data.add_attr(name, [])

    for line in open(fn).readlines():
        if line[0] == cmt:
            continue

        tmp = line.split()

        for col, name, fmt in specL:
            val = tmp[col]
            if fmt == "s":
                pass

            elif fmt == "f":
                val = float(val)

            elif fmt == "i":
                val = int(val)

            else:
                msg_err("Format unknown")

            data.get_attr(name).append(val)

    return data


def get_url(url, ofn=None, check_timestamp=False, timeout=5, tries=1):
    """Retrieve file from url
    """

    import os
    import time
    import urllib.request
    import urllib.error

    local_fn = url.split("/")[-1]

    if ofn == None:
        ofn = local_fn

    succeeded = False

    for n in range(tries):
        try:
            response = urllib.request.urlopen(url, timeout=timeout)

            # Check file timestamp

            if check_timestamp and os.path.exists(local_fn):

                # Find out remote file time in UTC
                # This is already in UTC
                remote_time = response.headers["last-modified"]
                remote_time = time.strptime(
                    remote_time, "%a, %d %b %Y %H:%M:%S %Z")
                watch(remote_time)

                # Find out local file time in UTC
                local_time = os.stat(local_fn).st_mtime
                local_time = time.gmtime(local_time)

                if remote_time < local_time:
                    break

            # Download file

            fl = open(ofn, "w")
            fl.write(response.read().decode("utf-8"))
            succeeded = True
            break

        except urllib.error.URLError:
            pass

    return succeeded


def wget(url, ofn=None, check_timestamp=False, no_check_certificate=False,
         timeout=None, tries=None):
    """
    Execute wget shell command

    Notes:

      1) set no_check_certificate=True when you have SSL 
         certification error
    """

    cmd = "wget"

    if ofn != None:
        cmd += " --output-document=%s" % (ofn)

    if no_check_certificate:
        cmd += " --no-check-certificate"

    if check_timestamp:
        cmd += " --timestamping"

    if timeout != None:
        cmd += " --timeout=%s" % (timeout)

    if tries != None:
        cmd += " --tries=%s" % (tries)

    cmd += " %s" % (url)

    s, o, e = exe_cmd(cmd, num_returns=3)

    return s, o, e
