#!/usr/bin/env python

import sys

from mbr import *
from Exfat import *
    
def icat(image):
    # On verifie que le premier argument est bien '-o'
    if(sys.argv[2] == "-o"):
        # Pour chaque partitions de la MBR :
        for partition in partitions:
            # Si le deuxieme argument correspond au debut d'une partition
            if(int(sys.argv[3]) == partition.first_sector):
                # Si cette partition est ExFAT
                if(partition.type == 0x07):
                    partition_start_offset = int(sys.argv[3])*512
                    partition_end_offset = partition_start_offset + (partition.size_in_sector*512)
                    exfat = Exfat(image[partition_start_offset:partition_end_offset])
                    entry = int(sys.argv[5])
                    # Si le quatrieme argument est un numero de cluster existant
                    if(entry in range(exfat.vbr.cluster_count)):
                        cluster_chain = exfat.fat.get_cluster_chain(entry)
                        file_meta = exfat.file_entry_sets.get(entry).sede.entry
                        if(sys.platform == "win32"):
                            import os, msvcrt
                            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                        sys.stdout.write(exfat.get_clusters(cluster_chain, file_meta.is_contiguous(), file_meta.data_length))
                        exit(0)
                    else:
                        print "Invalid inode adress: "+sys.argv[5]
                        exit(1)
                else:
                    print "unsupported file system"
                    exit(1)
        print "invalid image offset"
        exit(1)
    else:
        print "cannot determine file system type"
        exit(1)
