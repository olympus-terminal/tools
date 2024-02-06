from Bio import Entrez
import sys

## argv1 is query and argv is output. currently outputting top 20 hits

def fetch_sequence():
    Entrez.email = 'person@email.edu'   # Always tell NCBI who you are
    query = sys.argv[1]
    handle = Entrez.esearch(db='Gene', term=query)
    record = Entrez.read(handle)
    ids = record['IdList']
    if not ids:
        print("No sequences found. Please verify the gene name and organism.")
    else:
        id = ids[0:20] # or take more  # just take the first sequence
        handle = Entrez.efetch(db='gene', id=id, rettype='fasta', retmode='text')
        sequence = handle.read()
        print(sequence)  # print the sequence to console
        with open(sys.argv[2], 'w') as f:  # save to a file
            f.write(sequence)

if __name__ == '__main__':
    fetch_sequence()
