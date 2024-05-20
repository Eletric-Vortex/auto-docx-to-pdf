import os
import time
import re
from docx2pdf import convert
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def generateOutputFilename(filename: str, dest: str) -> str:
    filename = os.path.join(dest, os.path.splitext(os.path.basename(filename))[0] + ".pdf")
    return os.path.abspath(filename)


def Docx2Pdf(filename: str, dest: str) -> str:
    # conversion done
    convert(filename, dest)
    return generateOutputFilename(filename, dest)

class DocxHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if re.search(r'~\$.*\.docx$', event.src_path):
            return
    
        if event.src_path.endswith('.docx'):
            print(f"Converting {event.src_path} to PDF...")
            dest = os.path.dirname(event.src_path)
            output_filename = Docx2Pdf(event.src_path, dest)
            print(f"Converted to {output_filename}") 

def main(dest: str = os.getcwd()) -> None:
    observer = Observer()
    event_handler = DocxHandler()
    observer.schedule(event_handler, path=dest, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
if __name__ == "__main__":
    print("---->Welcome To Universal PDF Converter<----\n")
    main()