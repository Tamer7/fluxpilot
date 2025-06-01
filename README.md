# FluxPilot

FluxPilot is a powerful development environment launcher that helps you manage and run multiple development profiles with ease. Built with Python and CustomTkinter, it provides a clean and intuitive interface for launching your development workflows.

## Features

- **Profile Management**: Create, edit, and delete development profiles
- **Multi-step Execution**: Each profile can contain multiple commands that run sequentially
- **Real-time Console Output**: See live output from your running processes
- **Port Monitoring**: Built-in port checker to see what's running on your system
- **Tabbed Interface**: Run multiple profiles simultaneously in separate tabs
- **Process Management**: Start, stop, and monitor your development processes
- **Working Directory Support**: Set custom working directories for each command
- **Dark Theme**: Modern dark interface that's easy on the eyes

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tamer7/fluxpilot.git
   cd fluxpilot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run FluxPilot:
   ```bash
   python main.py
   ```

## Usage

### Creating a Profile

1. Click the **"Add"** button in the left panel
2. Enter a name for your profile
3. Add steps (commands) to your profile:
   - **Label**: A descriptive name for the step
   - **Command**: The command to execute
   - **Working Dir**: Optional working directory for the command
4. Click **"Save"** to create the profile

### Running a Profile

1. Select a profile from the list on the left
2. Click **"Run Selected"** to start the profile
3. Monitor the output in the console tab that opens
4. Use the **"Stop"** button to terminate all processes in the profile

### Managing Profiles

- **Edit**: Select a profile and click "Edit" to modify it
- **Delete**: Select a profile and click "Delete" to remove it
- **Port Check**: Click "Show Ports" to see active network connections

## Example Profile

Here's an example of a typical development profile:

**Profile Name**: "Full Stack Development"

**Steps**:
1. **Label**: "Start Database"  
   **Command**: `docker-compose up -d postgres`  
   **Working Dir**: `/path/to/your/project`

2. **Label**: "Start Backend API"  
   **Command**: `npm run dev`  
   **Working Dir**: `/path/to/your/project/backend`

3. **Label**: "Start Frontend"  
   **Command**: `npm start`  
   **Working Dir**: `/path/to/your/project/frontend`

## Configuration

Profiles are stored in `config/profiles.json`. You can manually edit this file if needed, but it's recommended to use the GUI for profile management.

## Requirements

- Python 3.8+
- CustomTkinter
- psutil

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Screenshots

<!-- Add screenshots here when available -->

## Roadmap

- [ ] Profile templates and sharing
- [ ] Environment variable management
- [ ] Log file export
- [ ] System tray integration
- [ ] Profile scheduling
- [ ] Docker integration improvements 