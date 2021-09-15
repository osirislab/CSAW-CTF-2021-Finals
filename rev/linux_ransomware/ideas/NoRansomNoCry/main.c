//
// Created by Aeon Flux (aka Mr. Snug) on 8/4/21.
//

#include <stdio.h>
#include <stdlib.h>


/*
 * mk = make key: takes in a buffer byte array (here containing all bytes of an entire file)
 * and create a key by copying the bytes starting from the end of the buffer array in reverse
 * order into a new key array, for which <keysize> memory space was reserved on the heap.
 */
unsigned char* mk(const char* buffer, int ks, long fs) {
	unsigned char* kA = malloc(ks * sizeof(unsigned char));
	unsigned char* kStat = kA;	// capture the start of the key

	for(long i = fs - 1; i >= (fs - ks); i--) {
		*kA = (unsigned char)buffer[i];
		kA++;
	}
	return kStat;
}


/*
 * simple function to display the bytes of the key. Omitted in the malware version.
 */
void showKey(const unsigned char* key, int keysize) {
	for(int i = 0; i < keysize; i++) {
		printf("%i: ", i);
		printf("%x\n", key[i]);
	}
}


/*
 * e = encrypt: receives the to be encrypted bytes in the buffer; gets a pointer to the key bytes;
 * encryption happens via plain XOR of every byte in the buffer with a byte of the key in sequence
 * first to last order; when the end of the key bytes is reached the key wraps around to the start;
 * write the resulting XOR'd bytes out to the encrypted file.
 */
void e(const char* buffer, const unsigned char* ky, long fl, int ks) {
	FILE* wp = fopen("efile.nrncry", "wb");	// Open the encrypted file for writing in binary mode
	int k = 0;								// set key counter to start of key
	for(int i = 0; i < fl; i++){			// loop through each bytes of the buffer
		char c = buffer[i] ^ ky[k];			// XOR buffer byte with k byte of the key
		fputc(c, wp);						// write out the XOR'd byte to file
		k++;								// move key counter up
		if (k == ks) { k = 0; }				// if keysize is reached, wrap around to start of key
	}
	fclose(wp);								// close file when done with all bytes in the buffer
}


/*
 * d = decrypt: receives the to be decrypted bytes in the buffer; gets a pointer to the key bytes;
 * decryption happens via plain XOR of every byte in the buffer with a byte of the key in sequence
 * first to last order; when the end of the key bytes is reached the key wraps around to the start;
 * write the resulting XOR'd bytes out to the decrypted file.
 *
 * CTF: This function will be empty in the malware version; the solution to the challenge is to
 * write the body of this function after reversing, analyzing, and understanding the method of
 * encryption and key generation.
 */
void d(const char* buffer, const unsigned char* ky, long fl, int ks) {
	FILE* wp = fopen("decf.jpg", "wb");		// Open the file for writing in binary mode
	int k = 0;								// set key counter to start of key
	for(int i = 0; i < fl; i++){			// loop through each bytes of the buffer
		char c = buffer[i] ^ky[k];			// XOR buffer byte with k byte of the key
		fputc(c, wp);						// write out the XOR'd byte to file
		k++;								// move key counter up
		if (k == ks) { k = 0; }				// if keysize is reached, wrap around to start of key
	}
	fclose(wp); 							// close file when done with all bytes in the buffer
}

/*
 * rf = read file: take in a filename and a pointer to store the file length, binary read in the
 * bytes of the file and return the pointer to the buffer on the heap where the bytes of the file
 * are stored.
*/
char* rf(char* fname, long* flen) {
	FILE* fileptr;
	char* buffer;
	long filelen;

	fileptr = fopen(fname, "rb");	// Open the file in binary mode
	fseek(fileptr, 0, SEEK_END);	// Jump to the end of the file
	filelen = ftell(fileptr);		// Get the current byte offset in the file
	*flen = filelen;				// Store the file length for use outside of this function
	rewind(fileptr);				// Jump back to the beginning of the file

	buffer = (char*)malloc(filelen * sizeof(char)); // Enough memory for the file
	fread(buffer, filelen, 1, fileptr); // Read in the entire file
	fclose(fileptr); // Close the file
	return buffer;
}


/*
 * wk = write key: simple function to write out the key's bytes into a file for testing & debug.
 * Omitted in malware version.
 */
void wk(const unsigned char* key, int keysize) {
	FILE* wp = fopen("key", "wb");
	for(int i = 0; i < keysize; i++){
		fputc(key[i], wp);
	}
	fclose(wp);
}

/*
 * alert: simple banner display function that shows the scary 'your files have been encrypted,
 * pay X BTC to a charity donation address
 */
void alert() {
	printf("oops, too bad we have encrypted all of your sensitive files. To get them back pay us some BTC.\n\n");
}


int main() {

	FILE *file;								// the flag file handle
	int ks = 256;							// set the key size
	long fl = 0;							// var to store the file length

	// read the program bytes into a buffer array, which we use to derive the key from. Since the
	// bytes of the program are already known, the key generation will be repeatable and most
	// importantly predictable
	char* kf = rf("NoRansomNoCry", &fl);
	unsigned char* k = mk(kf, ks, fl);		// make the key out of the buffer array
	//showKey(k, ks);						// show the key in console output
	wk(k, ks);								// write the key to a file

	// for safety only encrypt the flag file, if it exists and nothing else on the file system, otherwise exit
	file = fopen("flag.jpg", "r");
	if (file) {
		fclose(file);						// close the file so it's ready for reading into buffer
		fl = 0;                             // reset the file length var
		char *ff = rf("flag.jpg", &fl);     // read the original file content into a memory buffer
		printf("encrypting ... \n");
		e(ff, k, fl, ks);                   // encrypt the flag file data and write out to an encrypted file
		alert();                            // show the scary banner to the user
	} else {
		fclose(file);
	}

	// decrypt the encrypted flag file if it exists: OMITTED IN MALWARE VERSION
	file = fopen("efile.nrncry", "r");
	if (file) {
		fclose(file);
		fl = 0;        // reset the file length var
		char *eff = rf("efile.nrncry", &fl);      // read the encrypted flag file content into a memory buffer
		printf("decrypting ... \n");
		d(eff, k, fl, ks);                        // decrypt the encrypted flag file data and write out to a plain file
	} else {
		fclose(file);
	}

	return 0;
}
