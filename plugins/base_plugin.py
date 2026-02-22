from abc import ABC, abstractmethod

class BaseSocialPlugin(ABC):
    """
    Abstract Base Class for Social Media Plugins.
    All platform plugins must inherit from this class.
    """

    @abstractmethod
    def login(self, page, username, password):
        """
        Logic to perform manual login if session expires.
        """
        pass

    @abstractmethod
    def verify_login(self, page):
        """
        Logic to verify if the current session is valid.
        Returns: Boolean
        """
        pass

    @abstractmethod
    def post_content(self, page, content, media_path=None):
        """
        Logic to post content to the platform.
        Returns: Dict {'success': bool, 'message': str}
        """
        pass