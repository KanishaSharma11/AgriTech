import subprocess
import time

def run_app(file_path):
    print(f"Starting {file_path}...")
    # This will run the script and wait for it to finish.
    # To run it in the background, you would use a different method.
    process = subprocess.Popen(['python', file_path])
    return process

if __name__ == "__main__":
    files_to_run = [
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Crop Recommendation\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Crop Yield Prediction\crop_yield_app\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Crop_Planning\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Forum\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Labour_Alerts\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Crop_Prices_Tracker\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Community\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Fertilizer_recommendation\app.py",
        r"D:\MLPROJECTS\AgriTech-Main\AgriTech-main\Chat\backend\app.py"
    ]

    processes = []
    for file_path in files_to_run:
        processes.append(run_app(file_path))

    # Keep the main script running until all subprocesses finish
    try:
        while True:
            # You can add logic here to check on the processes
            # For simplicity, we'll just wait
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping all processes...")
        for p in processes:
            p.terminate()