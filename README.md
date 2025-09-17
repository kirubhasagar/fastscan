## Description
FastScan is a Python-based graphical application that scans a target IP address for open and closed ports. It provides real-time results, supports pausing/resuming scans, and maintains a history of previous scans.

## Features
- Scan single IP addresses for open/closed ports
- Specify custom port ranges
- Display host name information
- Pause and resume scans
- Maintain a scan history (view, save, load, clear)
- User-friendly GUI using Tkinter

## Technologies Used
- Python
- Tkinter (GUI)
- Socket programming
- Threading for responsive scanning
- JSON for history management

##UI

<img width="552" height="792" alt="image" src="https://github.com/user-attachments/assets/2da38719-3c65-47c2-81f3-ace7e19861fe" />


## Installation & Usage

### Clone the Repository
   Clone the GitHub repository to your local machine:

### Clone the Repository

Open your terminal and run:

     
        # Clone the FastScan repository
         git clone https://github.com/kirubhasagar/FastScan.git

        # Move into the project directory
         cd FastScan


### To Scan the Target
● Enter the target IP address in the **IP Address** field  
● For testing, you can use `127.0.0.1` (localhost)  
● Enter the port range in the **Port Range** field (e.g., `20-100`)  
● Click **Scan** to start scanning  
● Use **Pause/Resume** to control the scan if needed  

### Saving Scan History
● After scanning, click **Save History**  
● Choose a file location and name  
● The scan results will be saved as a **JSON file**, storing all scanned ports and their status  

<img width="923" height="112" alt="image" src="https://github.com/user-attachments/assets/417307d5-b34f-4b9e-b121-00a92615e942" />


### Loading Scan History

● Click Load History
● Select a previously saved JSON file
● The scan history will be loaded into the history box, allowing you to review results without rescanning

<img width="926" height="96" alt="image" src="https://github.com/user-attachments/assets/8b6a1c6e-b159-4cc6-916b-8c4756ffb060" />


---

### Thank You
Thank you for checking out **FastScan**!  
I hope this tool helps you understand how port scanning works and demonstrates the use of Python, Tkinter, threading, and networking concepts.  

Feel free to explore, test, and contribute. Any feedback or suggestions are highly appreciated!  

⭐ If you find this project useful, don’t forget to **star the repository**!

  


