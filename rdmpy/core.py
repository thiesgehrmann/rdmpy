import os
import pathlib
import datetime
import glob
import json

class RDM(object):
    _meta = {
        "source" : os.getcwd(),
        "user"   : os.getlogin()
    }
    
    def __init__(self, path, mode='w', file=False, nouser=False, suffix=True, modified=True, **meta):
        self.path = '/'.join(path.split('/')[:-1]) if len(path.split('/')) > 1 else '.'
        self.filename = path.split('/')[-1]
        self.prefix = '.'.join(self.filename.split('.')[:-1]) if suffix else self.filename
        self.suffix = self.filename.split('.')[-1] if suffix else None
        self.jsonfile = '%s/rdm_filedescriptions.json' % self.path
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        
        basemeta = self._meta.copy()
        basemeta.update(meta)
        meta = basemeta
        meta['basefile'] = self.filename
        
        self._session = {
            'mode' : mode,
            'file' : file,
            'meta' : meta,
            'modified' : modified,
            'nouser' : nouser
        }
    #edef
    
    @classmethod
    def meta(cls, **kwargs):
        cls._meta.update(kwargs)
    #edef
    
    def _glob(self, **kwargs):
        globstring = '{path}/{prefix}.{stamp}{dot}{suffix}'.format(
            path=self.path,
            prefix=self.prefix,
            stamp=self._rdmstamp(**kwargs)['stamp'],
            dot='.' if self.suffix is not None else '',
            suffix=self.suffix if self.suffix is not None else '')
        response = [ x.split('/')[-1] for x in sorted(glob.glob(globstring)) ]
        return response
    #edef
    
    def _rdmstamp(self, nouser=False, nodate=False):
        date = datetime.datetime.now().isoformat()
        user = os.getlogin()

        return {
            'user' : user,
            'created' : date,
            'modified' : date,
            'stamp' : 'rdm_{user}_{date}'.format(user=user if not nouser else '*', date=date if not nodate else '*').replace('.',':')
        }
    #edef

    def _rdmstamp_from_existing(self, filename):
        js = self._loadjson()
        
        if filename in js:
            meta = js[filename]
            return {
                'user' : meta['user'],
                'created' : meta['created'],
                'modified' : meta['modified'],
                'stamp' : 'rdm_{user}_{date}'.format(user=meta['user'], date=meta['created']).replace('.',':')
            }
        else:
            stamp = filename[::-1][:filename[::-1].find('_mdr.')][::-1].split('.')[0].split('_')
            return {
                'user'     : stamp[0],
                'created'  : stamp[1],
                'modified' : stamp[1],
                'stamp' : 'rdm_{user}_{date}'.format(user=stamp[0], date=stamp[1]).replace('.',':')
            }
        #fi
    #edef
    
    def __enter__(self):
        if self._session['mode'] not in ['r','w','rw']:
            raise NotImplementedError
        #fi
        
        if self._session['mode'] in [ 'r', 'rw' ]:
            g = self._glob(nouser=self._session['nouser'], nodate=True)

            stampnow = self._rdmstamp()
            self._session['stamp'] = self._rdmstamp_from_existing(g[-1]) if len(g) > 0 else stampnow
            self._session['meta']['created'] = self._session['stamp']['created']
            if self._session['modified']:
                if 'w' in self._session['mode']:
                    self._session['meta']['modified'] = stampnow['created']
                else:
                    self._session['meta']['modified'] = self._session['stamp']['modified']
                #fi
            else:
                self._session['meta']['modified'] = self._session['stamp']['modified']
            #fi
        #fi
        
        if self._session['mode'] == 'w':
            self._session['stamp'] = self._rdmstamp()
            self._session['meta']['created'] = self._session['stamp']['created']
            self._session['meta']['modified'] = self._session['stamp']['created']
        #fi
        
        self._session['filename'] = '{prefix}.{stamp}{dot}{suffix}'.format(
            prefix=self.prefix,
            stamp=self._session['stamp']['stamp'],
            dot='.' if self.suffix is not None else '',
            suffix=self.suffix if self.suffix is not None else '')
        
        self._session['filepath'] = '{path}/{prefix}.{stamp}{dot}{suffix}'.format(
            path=self.path,
            prefix=self.prefix,
            stamp=self._session['stamp']['stamp'],
            dot='.' if self.suffix is not None else '',
            suffix=self.suffix if self.suffix is not None else '')
        
        if self._session['file']:
            fd = open(session['filepath'], mode)
            self._session['fd'] = fd
            return fd
        #fi
        
        return self._session['filepath']
    #edef
    
    def _loadjson(self):
        if os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'r') as ifd:
                return json.loads(ifd.read())
            #ewith
        else:
            return {}
        #fi
    #edef
    
    def _writejson(self, d):
        with open(self.jsonfile, 'w') as ofd:
            ofd.write(json.dumps(d, indent='    ', sort_keys=True))
        #ewith
    #edef

    def __exit__(self, *args):
        if self._session['file']:
            self._session['fd'].close()
        #fi
        
        js = self._loadjson()
        
        nv = js.get(self._session['filename'],{})
        nv.update(self._session['meta'])
        js[self._session['filename']] = nv
        
        self._writejson(js)
    #edef
#eclass