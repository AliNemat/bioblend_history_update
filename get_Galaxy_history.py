

## A code which extracts infomration out of Galaxy instance by using bioblend, a library of API functions
## Ali Nematbaksh: ali.nematbakhsh@gmail.com

import argparse
import sys
import re
import pprint
import datetime
from operator import itemgetter
from bioblend.galaxy import GalaxyInstance
parser = argparse.ArgumentParser()
parser.add_argument('--workflow_name', dest='requested_workflow_name_info', required=False, default='none', help='The name of workflow which you want to gather information about')
parser.add_argument('--Galaxy_url', dest='input_galaxy_instance_url', required=True, help='The URL of instance of Galaxy')
parser.add_argument('--Galaxy_APIKey', dest='API_key', required = True,  help='API key of the Galaxy account to which the histories belong')
parser.add_argument('--Galaxy_url_write', dest='input_galaxy_instance_url_write', required = False, default='no_url', help='Galaxy url to write for output file if it is different than the one used in Galaxy_url')
args = parser.parse_args()

now = datetime.datetime.now()
gi = GalaxyInstance(url = args.input_galaxy_instance_url , key= args.API_key)
print ("**********************************************************************************************************")
print ("**********************************************************************************************************")
print ("**********************************************************************************************************")
print ("*** Requested name of workflow in Galaxy to search in history for metadata is: " + args.requested_workflow_name_info + "   **************")
print ("*** Considered Galaxy history is: " + args.input_galaxy_instance_url + "   ***********************************")
print ("*** Names of histories need to be in the format of: WorkFlowName-RunNmber-SampleID.AnalysisVersion   *****")
print ("**********************************************************************************************************")
print ("**********************************************************************************************************")
print ("**********************************************************************************************************")
print ("\n")

try:
    tmp_name = args.input_galaxy_instance_url.split(':')[1]
    galaxy_instance_name = tmp_name.split ('/')[-1]
except:
    print ("Warning: Galaxy url is not in proper format")
    galaxy_instance_name='galaxy_instance'

output_file_name= 'info_' + galaxy_instance_name +'_' +  args.requested_workflow_name_info + '_' + str (now.year) + str (now.month) + str (now.day) + str ( now.hour) + str( now.minute)+'.txt'
file_fastq_info  = open(output_file_name,'w')

histories = gi.histories.get_histories(deleted=False)

if (args.requested_workflow_name_info == 'none'):
    print ( "No name of workflow is given as input. The program is now searching for available workflows  \n"),
    workflows_name = []
    for h in histories :
        workflow_name = (h ['name'].split('-'))[0]
        if (workflow_name not in workflows_name):
            workflows_name.append (workflow_name)

    print ( "Name of workflows available in this instance of Galaxy is: \n"),
    for i in workflows_name: 
        print (i)
    
    print ("")
    print ( "Please choose one workflow and re-run the program"),
    sys.exit()


if (args.input_galaxy_instance_url_write == 'no_url'):
    args.input_galaxy_instance_url_write = args.input_galaxy_instance_url
    print ( "Galaxy_url is being used in the output files")

counter_fine_histories=0
counter_need_check_histories=0
counter_histories=0
name_ill_histories = []
samples_info = dict()
workflows_name = []
for h in histories :
    
    counter_histories += 1
    #if ( counter_histories > 1000) :
    #    break ; 
    history_passed_test = False  
    history_lookup = gi.histories.show_history(h['id'], contents=True)
    workflow_name = (h ['name'].split('-'))[0]

    if (workflow_name not in workflows_name):
        workflows_name.append (workflow_name)
    
    if (workflow_name  == args.requested_workflow_name_info):
        counter_R1_U=0
        counter_R1=0
        counter_R2_U=0
        counter_R2=0
        for hh in history_lookup :
            extension_format= hh.get ('extension', 'no extension exist')            
            if (extension_format == 'fastqsanger') :
                 if ('R1' in hh['name']):
                     counter_R1_U += 1
                     fastq_url_r1_id = hh['id'] 
                 if ('R2' in hh ['name']) :
                     counter_R2_U += 1
                     fastq_url_r2_id = hh['id'] 
                 
            if (extension_format == 'fastqsanger.gz') :
                 if ('R1' in hh['name']):
                     counter_R1 += 1
                     fastq_gz_url_r1_id = hh['id'] 
                 if ('R2' in hh ['name']) :
                     counter_R2 += 1
                     fastq_gz_url_r2_id = hh['id']

        if ( counter_R1 != 1 or counter_R2 != 1 or counter_R1_U != 1 or counter_R2_U != 1 ):
            print ( "Test1: Failed. In " + h ['name'] + " history, number of fastq/fastq.gz files is wrong") 
            print ("***************************************************************************************")
            counter_need_check_histories += 1
            name_ill_histories.append(h['name'])
            continue
        if ( counter_R1 == 1 and counter_R2 == 1 and counter_R1_U == 1 and counter_R2_U == 1 ):
            print ( "Test1: Passed. In " + h ['name'] + " hisory, number of fastq/fastq.gz files is fine" )
            try:
                run_id_sequencer                        = (h['name'].split('-'))[1]
                sample_id_and_analysis_version          = (h['name'].split('-'))[2]
                sample_id                               = (sample_id_and_analysis_version.split('.'))[0]
                analysis_version                        = (sample_id_and_analysis_version.split('.'))[1]
            except: 
                print ( "Test2: Failed." + h['name'] + " is not following the history naming conventation")
                print ("***************************************************************************************")
                counter_need_check_histories += 1
                name_ill_histories.append(h['name'])
                continue
            
                        
            print ( "Test2: Passed. Naming conventation is fine. History passed the two tests.\n")
            counter_fine_histories += 1
            history_passed_test = True
            print ( "Information of this history: ")
            print ( "workflow name: "), 
            print (workflow_name)
            print ( "sequencer run number: "),
            print (int (run_id_sequencer))
            print ( "sample id: "),
            print ( int(sample_id)) 
            print ( "analysis version for that sample: "),
            print ( int(analysis_version)) 
            print ("***************************************************************************************")
            #samples_info[ float(sample_id_and_analysis_version)] =  [h['name'], h ['id'], workflow_name, run_id_sequencer, fastq_url_r1_id, fastq_url_r2_id, fastq_gz_url_r1_id, fastq_gz_url_r2_id]     
            samples_info[ str(h['id'])] =  [float(sample_id_and_analysis_version), h['name'], h ['id'], workflow_name, run_id_sequencer, fastq_url_r1_id, fastq_url_r2_id, fastq_gz_url_r1_id, fastq_gz_url_r2_id]     



samples_info_values = samples_info.values()   
samples_info_values_sorted = sorted(samples_info_values, key = itemgetter(0))

if (args.input_galaxy_instance_url_write[-1] == '/'):
    args.input_galaxy_instance_url_write =args.input_galaxy_instance_url_write[:-1] 

file_fastq_info.write ('history_name, history_id, fastq_url_R1, fastq_url_R2, fastq.gz_url_R1, fastq.gz_url_R2 \n')
for sample in samples_info_values_sorted :
    file_fastq_info.write(sample[1]),
    file_fastq_info.write('  ')
    file_fastq_info.write(sample[2]),
    file_fastq_info.write('  ')
    file_fastq_info.write(args.input_galaxy_instance_url_write + '/datasets/' + sample[5] + '/display?preview=True' ),
    file_fastq_info.write('  ')
    file_fastq_info.write(args.input_galaxy_instance_url_write + '/datasets/' + sample[6] + '/display?preview=True' ),
    file_fastq_info.write('  ')
    file_fastq_info.write(args.input_galaxy_instance_url_write + '/datasets/' + sample[7] + '/display?preview=True' ),
    file_fastq_info.write('  ')
    file_fastq_info.write(args.input_galaxy_instance_url_write + '/datasets/' + sample[8] + '/display?preview=True' )
    file_fastq_info.write('  \n')

file_fastq_info.close() 


print ("***************************************************************************************")
print ("***************************************************************************************")
print ("Number of fine histories  corresponding to workflow: " + args.requested_workflow_name_info  + "is: " + str(counter_fine_histories))
print ("Number of ill  histories  corresponding to workflow: " + args.requested_workflow_name_info  + "is: " + str(counter_need_check_histories))
print ("Total number of histories is: " + str(counter_histories))
print ("***************************************************************************************")
print ("***************************************************************************************")

for name_ill_history in name_ill_histories :
    print ( str (name_ill_history) + " needs to be cheked" )


print ("***************************************************************************************")
print ("***************************************************************************************")

print ( "Name of workflows available in this instance of Galaxy is: \n"),
for i in workflows_name: 
    print (i)
    

print ("\n")
print ("**********************************************************************************************************")
print ("*************************************** Analysis successfully finished ***********************************")
print ("**********************************************************************************************************")



  

