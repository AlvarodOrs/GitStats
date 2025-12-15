import subprocess
import os
from typing import Optional
from datetime import datetime
from .tools import update_json

class GitUpdater:
    """Handles automatic Git commits and pushes"""
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize Git updater
        
        Args:
            repo_path: Path to the Git repository (default: current directory)
        """
        self.repo_path = repo_path
        self.repo_path_base = os.path.basename(os.path.abspath(self.repo_path))
        if self.repo_path_base != "GitStats": raise Exception(f"Careful, the processes are being run on: {os.path.abspath(self.repo_path)}")

    def run_command(self, command: list) -> tuple[bool, str]:
        """
        Run a Git command and return success status and output
        
        Args:
            command: List of command parts (e.g., ['git', 'status'])
            
        Returns:
            (success: bool, output: str)
        """
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            print(result)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def check_git_installed(self) -> bool:
        """Check if Git is installed"""
        success, _ = self.run_command(['git', '--version'])
        return success
    
    def check_is_git_repo(self) -> bool:
        """Check if current directory is a Git repository"""
        success, _ = self.run_command(['git', 'rev-parse', '--git-dir'])
        return success
    
    def check_git_remote(self) -> bool:

        success, _ = self.run_command(['git', 'remote', '-v'])
        return success
    
    def has_changes(self, file_paths: list[str]) -> bool:
        """
        Check if specified files have changes
        
        Args:
            file_paths: List of file paths to check
            
        Returns:
            True if any files have changes
        """
        for file_path in file_paths:
            success, output = self.run_command(['git', 'status', '--porcelain', file_path])
            if success and output.strip():
                return True
        return False
    
    def stage_files(self, file_paths: list[str]) -> bool:
        """
        Stage files for commit
        
        Args:
            file_paths: List of file paths to stage
            
        Returns:
            True if successful
        """
        success, output = self.run_command(['git', 'add'] + file_paths)
        if success:
            print(f"Staged files: {', '.join(file_paths)}")
        else:
            print(f"Failed to stage files: {output}")
        return success
    
    def commit(self, message: str) -> bool:
        """
        Create a Git commit
        
        Args:
            message: Commit message
            
        Returns:
            True if successful
        """
        success, output = self.run_command(['git', 'commit', '-m', message])
        if success:
            print(f"Created commit: {message}")
        else:
            print(f"Failed to commit: {output}")
        return success
    
    def push(self, remote: str = 'origin', branch: Optional[str] = None) -> bool:
        """
        Push commits to remote
        
        Args:
            remote: Remote name (default: 'origin')
            branch: Branch name (default: current branch)
            
        Returns:
            True if successful
        """
        # Get current branch if not specified
        if branch is None:
            success, output = self.run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
            if not success:
                print(f"Failed to get current branch: {output}")
                return False
            branch = output.strip()
        
        # Push to remote
        success, output = self.run_command(['git', 'push', remote, branch])
        if success:
            print(f"Pushed to {remote}/{branch}")
        else:
            print(f"Failed to push: {output}")
        return success
    
    def commit_and_push(
        self, 
        file_paths: list[str], 
        commit_message: str,
        remote: str = 'origin',
        branch: Optional[str] = None
    ) -> bool:
        """
        Stage, commit, and push files in one operation
        
        Args:
            file_paths: List of file paths to commit
            commit_message: Commit message
            remote: Remote name (default: 'origin')
            branch: Branch name (default: current branch)
            
        Returns:
            True if all operations successful
        """
        # Validation checks
        if not self.check_git_installed():
            print("Git is not installed")
            return False
        
        if not self.check_is_git_repo():
            print("Not a Git repository")
            return False
        
        # Check if files have changes
        if not self.has_changes(file_paths):
            print("No changes to commit")
            return True
        
        if not self.check_git_remote():
            print("Not correct remote repo")
            return False
        
        # Stage files
        if not self.stage_files(file_paths):
            return False
        
        # Commit
        if not self.commit(commit_message):
            return False
        
        # Push
        if not self.push(remote, branch):
            return False
        
        update_json('data/auto-commits.json')

        return True


def auto_update_github(
    file_paths: list[str],
    commit_message: str = "#GitStats card update#",
    repo_path: str = ".",
    remote: str = "origin",
    branch: Optional[str] = None
) -> bool:
    """
    Convenience function to automatically commit and push changes
    
    Args:
        file_paths: List of file paths to commit
        commit_message: Commit message (default: "#GitStats card update#")
        repo_path: Path to Git repository (default: current directory)
        remote: Remote name (default: 'origin')
        branch: Branch name (default: current branch)
        
    Returns:
        True if successful
    
    Example:
        >>> auto_update_github(['img/stats-card.svg', 'data/stats.json'])
    """
    updater = GitUpdater(repo_path)
    return updater.commit_and_push(file_paths, commit_message, remote, branch)