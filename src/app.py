import os
from src.arena import InterfaceManager, Config

def main():
    """
    Initialize and launch the application.

    Creates the configuration, sets up the interface manager, and launches the web interface.
    """
    # Load configuration
    config = Config()

    # Create interface manager
    interface = InterfaceManager(config)

    # Launch the interface
    interface.demo.launch(
        share=False,
        # ssl_certfile=os.getenv("SSL_CERT_FILE"),
        # ssl_keyfile=os.getenv("SSL_KEY_FILE")
    )

if __name__ == "__main__":
    main()
