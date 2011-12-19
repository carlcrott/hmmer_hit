import os, urllib, urllib2

def hmmer_hit(seq, hmmer_db, file_name, RNAflag=False):
  """Function expects: string sequence, string representaion for a HMMER database, string file name for output and boolean True if RNA. Check code for example function calls"""

  # Examples:
  # hmmer_modules.hmmer_hit("ACUGCCUGGAC", "nr" , "test_output.txt", True) 
  # hmmer_modules.hmmer_hit(">Seq\nKLRVLGYHNGEWCEAQTKNGQGWVPSNYITPVNSLENSIDKHSWYHGPVSRNAAEY", "pdb" , "output.txt") 
  # The value passed in for "hmmer_db" can be any of HMMERs databases: 
  # "env_nr", "nr", "pdb", "swissprot", "unimes", "uniprotkb"

  filepath = os.path.join(os.path.expanduser("~"), file_name)

  #========================  Yanked from HMMER tutorial ============================

  # install a custom handler to prevent following of redirects automatically.
  class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
      def http_error_302(self, req, fp, code, msg, headers):
          return headers

  opener = urllib2.build_opener(SmartRedirectHandler())
  urllib2.install_opener(opener);

  parameters = {'seqdb':hmmer_db ,'seq': seq }
  enc_params = urllib.urlencode(parameters);

  #post the search request to the server
  request = urllib2.Request('http://hmmer.janelia.org/search/phmmer', enc_params)

  # unlike the previous version of the code this will search through the headers
  # for a "location" instead of just guessing at the placement of the wanted URL
  # within the header structure
  results_url = urllib2.urlopen(request).getheaders('location')[0]

  # modify the range, format and presence of alignments in your results here
  # if using JSON you can use pretty output:
  # http://docs.python.org/library/json.html
  res_params = {'output':'json', 'range':'1,10' }

  # add the parameters to your request for the results
  enc_res_params = urllib.urlencode(res_params)
  modified_res_url = results_url + '?' + enc_res_params

  # send a GET request to the server
  results_request = urllib2.Request(modified_res_url)

  data = urllib2.urlopen(results_request)

  #===========================  End HMMER tutorial =============================

  output_file = open(filepath,'w')
  output_file.write(data.read())
  


