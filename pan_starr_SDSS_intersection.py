
import astropy as apy
import os
import csv
import requests
from pathlib import Path
import re
import numpy as np
import math

class CrossMatch(object):

    @staticmethod
    def _cross_sp(path = "/Users/jaylenluc/Desktop/spin-parity-catalog/original/galaxies" : str, path_pan = '/Users/jaylenluc/Desktop/cora_task/pan_starrs.tsv' : str,) -> None:

        from intersection_dict import sdss_dict
        #writer = open('intersection.txt', 'w')
        path = Path(path)
        #writer_no = open('no_intersection.txt','w')
        writer_log = open('all_gax.txt','w')
        tsv_write = open(path_pan, 'w')
        tsv_write.write('ra\tdec\tname\n')

        #['NGC2742 ', 'ra ', ' 136.889710', 'dec ', ' 60.479330', '\n']
        for table in path.iterdir():
            if not table.name.startswith('.'):
                writer_log.write(f'{table.name}----------------------------------- \n')
                for galaxy in table.iterdir():
                    if not galaxy.name.startswith('.'):
                        writer_log.write(f'{galaxy.name} \n')
                        for i in galaxy.iterdir():
                            if "_ra_dec.txt" in i.name:
                                #0 : name , 2 : ra, 4 : dec
                                li = re.split(r'=|\(|\)|, ',open(i, 'r').read())
                                tsv_write.write(f'{li[2]}\t{li[4]}\t{li[0]}\n')
        #writer.close()
        tsv_write.close()
        print('done')

#------------------------------------------------------------------------------------------------------------------
    #pan starrs = 525
    #sdss = 893212
    @staticmethod
    def best_match() -> None: 
        #CONSTUCTION
        sdss_array = [] # ra, dec,dr7obwjid 
        pan_array = [] # ra, dec, name
        sdss_name_match = []
        pan_name_match = []
        cross_match_log = open('crossmatches_log.csv','w')
        cross_match_log.write('PanStarrs_name,dr7objid,ra_panstarr,dec_panstarr,ra_sdss,dec_sdss,spherical_cos_distance\n')
        #POPULATION
        with open('Kelly-Final-GZ-all.tsv') as sdss, open('pan_starrs.tsv') as pan_starr:
             
            sdss_reader = csv.DictReader(sdss, delimiter='\t')

            #ra, dec ID
            pan_starr_reader = csv.DictReader(pan_starr, delimiter= '\t')
            #'ra','dec'
            #[name, ra, dec]
            #[d7id, ra, dec]
            for row in pan_starr_reader:
                if row['ra'] != 'null':
                    pan_array.append( [((math.pi/180) * float(row['ra'])),((math.pi/180) * float(row['dec']))] ) 
                    pan_name_match.append(row['name'])
            for row in sdss_reader:
                if row['ra'] != 'null':
                    sdss_array.append([((math.pi/180) * float(row['ra'])),((math.pi/180) * float(row['dec']))])
                    sdss_name_match.append( row['dr7objid'])
             
            
        
        #find cosine distance for all of panstarrs parall processing
        #_1 = sdss, _2 = panstarrs
        sdss_array = np.array(sdss_array)
        pan_array = np.array(pan_array)
        #print(type(sdss_array[3,1])
        sin_1 = np.sin(sdss_array[:,1])
        cos_1 = np.cos(sdss_array[:,1])
        ra_1 = sdss_array[:,0] 
        for ind, row in enumerate(pan_array):
            #print('fdsafda')
            dist_array = (sin_1*np.sin(row[1])) + ((cos_1 * np.cos(row[1])) * np.cos(ra_1 - row[0]))
            closest_dist_ind = np.argmax(dist_array)
            cross_match_log.write(f'{pan_name_match[ind]},{sdss_name_match[closest_dist_ind]},{row[0]},{row[1]},{sdss_array[closest_dist_ind,0]},{sdss_array[closest_dist_ind,1]},{dist_array[closest_dist_ind]}\n')
        #(ra_1,dec_1), (dec_1, dec_2)
        #cosine distance = cos(theta) = sin_1(dec_1)*sin_2(dec_2) + (cos_1(dec_1) * cos_2(dec_2)*cos_3(ra_1-ra_2))
        #write(f'PanStarrs_name,dr7objid, ra_panstarr, dec_panstarr, ra_sdss, dec_sdss, spherical_distance') 
        #crosscheck

        cross_match_log.close()
if __name__ == "__main__":
    #have Kelly-Final-GZ-all.tsv and pan_starrs.tsv
    #CrossMatch._cross_sp(your_path_to_original/galaxies)
    CrossMatch.best_match()




















