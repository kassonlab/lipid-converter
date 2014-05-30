import cloudstorage as gcs

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=300,
                                          urlfetch_timeout=600)

gcs.set_default_retry_params(my_default_retry_params)

BUCKET = '/lipid-converter/'

def create_file(filename):
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)

    return gcs_file


def create_file_and_write(f,filename):
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    
    
    #if isinstance(f,str):
    #    gcs_file.write('%s'%f)
    #else:
    data = f.read(65536)
    while data:
        gcs_file.write(data)
        data=f.read(65536)
    #gcs_file.write(f)
    #gcs_file.write(f)
    #gcs_file.write('f'*1024*1024 + '\n')
    gcs_file.close()
    #self.tmp_filenames_to_clean_up.append(filename)     
    

def read_file(filename):
    #print "read_FILE"
    filename = BUCKET + filename
    #self.response.write('Truncated file content:\n')
    gcs_file = gcs.open(filename,'r')
    foo = gcs_file.read().split('\n')
    foo = '\n'.join(foo)
     #for f in foo: 
     #    print f
     #print foo[3]
     #for line in gcs_file.read():
     #    print line
     #print gcs_file.readline()
     #self.response.write(gcs_file.readline()) 
     #gcs_file.seek(-1024, os.SEEK_END) 
     #self.response.write(gcs_file.read())              
    gcs_file.close()
    #print "FOO"
    return foo

def stat_file(filename):
    stat = gcs.stat(BUCKET+filename)
    print stat

def list_bucket(bucket):
     page_size=1
     stats = gcs.listbucket(bucket, max_keys=page_size)
     
     for stat in stats:
         print stat
         
def save_to_cloud(f,filename):
      filename = BUCKET + filename
      
      #print filename
      create_file_and_write(f,filename)

