import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class GitClient:
    """Handles Git operations."""
    
    def __init__(self, repo_path: Path = Path(".")):
        """
        Initialize Git client.
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = repo_path
        
        if not self._is_git_repo():
            raise ValueError(f"Not a Git repository: {repo_path}")
    
    def _run_command(self, command: list[str]) -> tuple[bool, str]:
        """
        Run a Git command.
        
        Args:
            command: Command parts
            
        Returns:
            (success, output)
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)}")
            logger.error(f"Error: {e.stderr}")
            return False, e.stderr
    
    def _is_git_repo(self) -> bool:
        """Check if directory is a Git repository."""
        success, _ = self._run_command(['git', 'rev-parse', '--git-dir'])
        return success
    
    def has_changes(self, files: list[Path]) -> bool:
        """
        Check if files have uncommitted changes.
        
        Args:
            files: Files to check
            
        Returns:
            True if any file has changes
        """
        for file in files:
            success, output = self._run_command([
                'git', 'status', '--porcelain', str(file)
            ])
            if success and output:
                return True
        return False
    
    def stage(self, files: list[Path]) -> bool:
        """
        Stage files for commit.
        
        Args:
            files: Files to stage
            
        Returns:
            True if successful
        """
        file_paths = [str(f) for f in files]
        success, output = self._run_command(['git', 'add'] + file_paths)
        
        if success:
            logger.info(f"Staged {len(files)} files")
        else:
            logger.error(f"Failed to stage files: {output}")
        
        return success
    
    def commit(self, message: str) -> bool:
        """
        Create a commit.
        
        Args:
            message: Commit message
            
        Returns:
            True if successful
        """
        success, output = self._run_command(['git', 'commit', '-m', message])
        
        if success:
            logger.info(f"Created commit: {message}")
        else:
            logger.error(f"Failed to commit: {output}")
        
        return success
    
    def push(
        self,
        remote: str = 'origin',
        branch: Optional[str] = None
    ) -> bool:
        """
        Push commits to remote.
        
        Args:
            remote: Remote name
            branch: Branch name (default: current)
            
        Returns:
            True if successful
        """
        if branch is None:
            success, branch = self._run_command([
                'git', 'rev-parse', '--abbrev-ref', 'HEAD'
            ])
            if not success:
                logger.error("Failed to get current branch")
                return False
        
        success, output = self._run_command(['git', 'push', remote, branch])
        
        if success:
            logger.info(f"Pushed to {remote}/{branch}")
        else:
            logger.error(f"Failed to push: {output}")
        
        return success
    
    def commit_and_push(
        self,
        files: list[Path],
        message: str,
        remote: str = 'origin',
        branch: Optional[str] = None
    ) -> bool:
        """
        Stage, commit, and push files.
        
        Args:
            files: Files to commit
            message: Commit message
            remote: Remote name
            branch: Branch name
            
        Returns:
            True if successful
        """
        if not self.has_changes(files):
            logger.info("No changes to commit")
            return True
        
        if not self.stage(files):
            return False
        
        if not self.commit(message):
            return False
        
        if not self.push(remote, branch):
            return False
        
        return True