#!/usr/bin/python

1. Jmp instruction
2. Signature: « EXFAT »
3. VBR1 address= sector number: 0x33 (début disque) = 0x33*512=0x6600
4. Total volume size in sectors: 0xED4D = 32mo
5. Address of FAT#1: secteur 0x80 (+VBR)
6. Size of FAT: 0x40 sectors
7. Data/cluster region address: 0x100 (+VBR)
8. Number of Cluster number in the Cluster heap
9. Cluster address of root dir: 5
10. Volume S/N
11. exFat version: 1.0
12. Flags
13. Bytes per sectors: 9 (2^9 = 512 bytes)
14. Sectors per clusters: 3 (2^3 = 8)
15. End of bootcode
16. Synchro fin de secteur



fat_address
fat_size
cluster_region_address
root_cluster_address

byte_per_cluster



vbr = [

 
addr_fat1 
fat_size 
addr_data_region
cluster_num
root_cluster
serial_num
sector_size
cluster_size


def __init__(self, vbr_offset)
	dump = open("dump.raw", "r")
	dump.seek(vbr_offset)
	vbrcontent = dump.read(512)

	signature = vbrcontent[3:10]
	addr_vbr1 = vbr_offset
	taille_vol = vbrcontent[]
	taille_vol = vbr_offset + (12*512)
	addr_fat1 = vbrcontent[80:84]
	fat_size = vbrcontent[84:88]
	addr_data_region = 
	cluster_num 
	bytes_per_sector = vbrcontent[109:109]
	sect_per_cluster = vbrcontent[109:110]
	root_cluster = 
	serial_num
	sector_size
	cluster_size



73 8