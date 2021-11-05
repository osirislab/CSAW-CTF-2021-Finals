# Directory Enumeration

Enumerate the directories using either Proxychains with tools like dirb or dirbuster.  Another useful tool is dirstalk.  Just specify the socks5 port to 9150 or 9050 (depending on how you setup tor)

Once enumerated, you will find the following:
  hidden -> empty directory
  backups -> contains alice.jpg and lookharder.pdf
  
## Rabbit Hole

The jpg file contains a hidden file (rabbit.txt) that can be extracted using steghide.jpg.  The contents of this file points to a twitter handle.  Currently, this handle does not contain any useful information.

# Hidden Flag

The flag is actually found in lookharder.pdf.  The solution can be found in blog.didierstevens.com/2009/07/01/embedding-and-hiding-files-in-pdf-documents.  Modifying the pdf file as shown in the blog, you can extract the flag using a PDF reader such as Adobe Acrobat and extracting the attached file (flag.txt)
