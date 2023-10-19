<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Gesture Control ✋💡</h3>

  <p align="center">
    Manage Philips Hue Lights with Hand Gestures
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#run-the-application">Run The Application</a></li>  
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Gesture Control is a project that empowers you to control your Philips Hue lights using hand gestures. 

### Built With

- [Python](https://www.python.org/)
- [MediaPipe](https://developers.google.com/mediapipe)
- [OpenCV](https://opencv.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/iammatthi/gesture-control.git
   ```
2. Move into the newly created folder
   ```sh
   cd gesture-control
   ```
3. Configure the application
    - Use automatic configuration (recommended)
        ```sh
        chmod +x configure.sh
        ./configure.sh
        ```
    - Use manual configuration
        1. Create virtual environment
        ```sh
        python3 -m venv venv
        ```
        2. Activate virtual environment
        ```sh
        source venv/bin/activate
        ```
        3. Install dependencies
        ```sh
        pip install -r requirements.txt
        ```
        4. Download gesture recognition model
            ```sh
            mkdir models
            wget -q https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task -O models/gesture_recognizer.task
            ```
        5. Create and edit `config.yml` file (see [`config.yml.example`](config.yml.example) for an example)
            - Follow [this](https://developers.meethue.com/develop/get-started-2/) guide to get all information needed for the config file

<!-- USAGE EXAMPLES -->

## Run The Application
Make sure you have a virtual environment activated (`source venv/bin/activate`). Then run the following command:
```bash
python main.py
```

Now you can control your lights with hand gestures. The following gestures are supported:
- ✊: Turn lights on
- ✋: Turn lights off
- 👍: Increase brightness
- 👎: Decrease brightness
