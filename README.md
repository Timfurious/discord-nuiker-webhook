# discord nuker
Send, test, and manage Discord webhooks with speed, style, and HTTPS proxy support.

WebhookBlaster is a powerful Python-based command-line tool designed for interacting with Discord webhooks. It enables users to send high-frequency messages (Nuke mode), test webhook connectivity, delete webhooks, and manage HTTPS proxies with automatic rotation. With 

a sleek interface featuring color gradients, robust error handling, and support for both public and custom proxies, WebhookBlaster is ideal for developers, automation enthusiasts, and anyone looking to streamline webhook operations.

Features

High-Frequency Messaging (Nuke Mode): Send POST messages to Discord webhooks at customizable intervals (minimum 100ms) with automatic HTTPS proxy rotation to bypass rate limits.

Webhook Management: Easily test webhook connectivity or delete webhooks with a single command.

HTTPS Proxy Support: Automatically fetches and tests public HTTPS proxies from multiple sources (e.g., ProxyScrape, Free Proxy List) and allows adding custom proxies.

Proxy Rotation: Seamlessly rotates through valid proxies for each request to enhance reliability and anonymity.

Robust Error Handling: Manages Discord rate limits (HTTP 429), network errors, and invalid inputs with clear, user-friendly messages.

Stylish CLI Interface: Features smooth blue-to-purple color gradients for an engaging user experience.

Modular Design: Well-organized code with reusable functions, making it easy to extend or maintain.

Debugging Support: Detailed logging for proxy testing to diagnose issues with public or custom proxies.


Installation

Prerequisites

Python: Version 3.6 or higher.

Dependencies: requests, colorama.

Setup Instructions

Clone the Repository:git clone https://github.com/yourusername/WebhookBlaster.git


Install Dependencies:pip install requests colorama


Run the Program



Usage

Launch the Program:

Run the script, and it will prompt you to enter a valid Discord webhook URL (e.g., https://discord.com/api/webhooks/...).

The tool automatically fetches public HTTPS proxies and tests them for compatibility. If no valid proxies are found, it prompts you to add a custom proxy.


Menu Options:

HTTPS proxies in use: X

1. Send messages (Nuke)
2. Delete webhook
3. Test webhook
4. Add custom proxy
5. Show help
6. Exit


Send Messages (Nuke): Send repeated POST messages with a custom message and username, using proxy rotation to avoid rate limits.

Delete Webhook: Permanently delete the specified webhook.

Test Webhook: Verify if the webhook is active and reachable.

Add Custom Proxy: Input a custom HTTPS proxy (e.g., http://123.45.67.89:8080) to include in the rotation.

Show Help: Display available commands and their descriptions.

Exit: Quit the program.


Example Workflow:

Start the program and enter a Discord webhook URL.

If no proxies are found, select option 4 to add a custom proxy.

Choose option 1 to send messages, specifying the message content, bot username, and frequency.

Monitor the output for success messages or error details (e.g., rate limits, network issues).




Proxy Management

Public Proxies: The tool fetches HTTPS-compatible proxies from reliable sources like ProxyScrape and Free Proxy List, testing each for speed and compatibility.

Custom Proxies: Add your own proxies via the "Add custom proxy" option. Proxies are validated for HTTPS support before being added to the rotation pool.

Rotation: Proxies are automatically rotated for each request to enhance reliability and avoid IP-based restrictions.

Debugging: Detailed logs show why proxies fail (e.g., timeout, connection error), helping you troubleshoot issues.


Note: Public proxies can be unreliable. For better performance, consider using paid proxy services (e.g., Bright Data, Oxylabs) and adding them via the custom proxy option.

Troubleshooting

No Proxies in Use:

If "HTTPS proxies in use: 0" appears, the program failed to find valid public proxies. Use option 4 to add a custom proxy or check your network connection.

Run a network test:import requests

try:
    response = requests.get("https://httpbin.org/ip", timeout=10)
    
    print("Network test successful:", response.status_code)
    
except Exception as e:

    print("Network test failed:", e)
    


Ensure your firewall or ISP isn’t blocking proxyscrape.com or httpbin.org.



Rate Limits:

The tool handles Discord’s rate limits (HTTP 429) by waiting the specified retry_after time.

If rate limits persist, increase the message frequency or add more proxies.


Invalid Webhook URL:

Ensure the URL starts with https://discord.com/api/webhooks/ or https://discordapp.com/api/webhooks/.



Contributing

Contributions are welcome! To contribute:

Fork the repository.

Create a feature branch (git checkout -b feature/your-feature).

Commit your changes (git commit -m 'Add your feature').

Push to the branch (git push origin feature/your-feature).

Open a pull request.

Please include a detailed description of your changes and ensure the code follows the project’s style (e.g., consistent comments, modular structure).

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

Built with Python, requests, and colorama.

Proxy sources: ProxyScrape, Free Proxy List.

Inspired by the need for a fast, reliable, and stylish webhook automation tool.
