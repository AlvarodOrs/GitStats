class Profile: # GithubProfile(profile _data)
    def __init__(self, profile_data: dict):
        self.profile_data = profile_data
    
    def login(self) -> str:
        return self.profile_data.get("login", "get_login_failed")
    
    def id(self) -> int:
        return self.profile_data.get("id", -1)
    
    def node_id(self) -> str:
        return self.profile_data.get("node_id", "get_node_id_failed")
    
    def avatar_url(self) -> str:
        from utils.tools import encode_to_64
        avatar_url = self.profile_data.get("avatar_url", "get_avatar_url_failed")
        return encode_to_64(avatar_url)
    
    def gravatar_id(self) -> str:
        return self.profile_data.get("gravatar_id", "get_gravatar_id_failed")
    
    def url(self, _type: str = '') -> str:
        """_type options:
            None (returns 'url'),
            'html', 'followers', 'following', 'gists', 'starred',
            'subscriptions', 'organizations', 'repos', 'events', 'received_events'
        """
        return self.profile_data.get(f"{_type}_url", f"get_{_type}_url_failed")
        
    def type(self) -> str:
        return self.profile_data.get("type", "get_type_failed")
    
    def user_view_type(self) -> str:
        return self.profile_data.get("user_view_type", "get_site_admin_failed")
    
    def is_site_admin(self) -> bool:
        return self.profile_data.get("site_admin", False)
    
    def name(self) -> str:
        return self.profile_data.get("name", "get_name_failed")
    
    def company(self) -> str:
        return self.profile_data.get("company", "get_company_failed")
    
    def blog(self) -> str:
        return self.profile_data.get("blog", "get_blog_failed")
    
    def location(self) -> str:
        return self.profile_data.get("location", "get_location_failed")
    
    def email(self) -> str:
        return self.profile_data.get("email", "get_email_failed")
    
    def hireable(self) -> bool:
        return self.profile_data.get("hireable", False)
    
    def bio(self) -> str:
        return self.profile_data.get("bio", "get_bio_failed")
    
    def twitter_username(self) -> str:
        return self.profile_data.get("twitter_username", "get_twitter_username_failed")
    
    def notification_email(self) -> str:
        return self.profile_data.get("notification_email", "get_notification_email_failed")
    
    def public_repos_count(self) -> int:
        return self.profile_data.get("public_repos", 0)
    
    def public_gists_count(self) -> int:
        return self.profile_data.get("public_gists", 0)
    
    def followers_count(self) -> int:
        return self.profile_data.get("followers", 0)
    
    def following_count(self) -> int:
        return self.profile_data.get("following", 0)
    
    def created_at(self) -> str:
        return self.profile_data.get("created_at", "get_created_at_failed")
    
    def updated_at(self) -> str:
        return self.profile_data.get("updated_at", "get_updated_at_failed")
    
class Repository: # GithubRepository(repo_data)
    def __init__(self, repo_data: dict):
        self.repo_data = repo_data
    
    def id(self) -> int:
        return self.repo_data.get("id", -1)
    
    def node_id(self) -> str:
        return self.repo_data.get("node_id", "get_node_id_failed")
    
    def name(self) -> str:
        return self.repo_data.get("name", "get_name_failed")
    
    def full_name(self) -> str:
        return self.repo_data.get("full_name", "get_full_name_failed")

    def private(self) -> bool:
        return self.repo_data.get("private", False)
    
    def owner(self, _type: str = 'all') -> str:
        """_type options: samme as GitHubProfile class methods until 'is_site_admin()' (included)"""
        owner_data = self.repo_data.get("owner", {"get_owner_failed": True})
        if _type == 'all':
            return owner_data
        return owner_data.get(_type, f"get_owner_{_type}_failed")
    
    def url(self, _type: str = '') -> str:
        """_type options:
            None (returns 'url'),
            'html', 'forks', 'keys', 'collaborators', 'teams', 'hooks',
            'issue_events', 'events', 'assignees', 'branches', 'tags',
            'blobs', 'git_tags', 'git_refs', 'trees', 'statuses',
            'languages', 'stargazers', 'contributors', 'subscribers',
            'subscription', 'commits', 'git_commits', 'comments',
            'issue_comment', 'contents', 'compare', 'merges',
            'archive',  'downloads',  'issues',  'pulls',
            'milestones',  'notifications',  'labels',  'releases',
            'deployments', 'git', 'ssh', 'clone', 'svn'
        """
        return self.repo_data.get(f"{_type}_url", f"get_{_type}_url_failed")
    
    def description(self) -> str:
        return self.repo_data.get("description", "get_description_failed")
    
    def is_fork(self) -> bool:
        return self.repo_data.get("fork", False)
    
    def created_at(self) -> str:
        return self.repo_data.get("created_at", "get_created_at_failed")
    
    def updated_at(self) -> str:
        return self.repo_data.get("updated_at", "get_updated_at_failed")
    
    def pushed_at(self) -> str:
        return self.repo_data.get("pushed_at", "get_pushed_at_failed")
    
    def homepage(self) -> str:
        return self.repo_data.get("homepage", "get_homepage_failed")
    
    def size(self) -> int:
        return self.repo_data.get("size", -1)
    
    def stargazers_count(self) -> int:
        return self.repo_data.get("stargazers_count", -1)

    def watchers_count(self) -> int:
        return self.repo_data.get("watchers_count", -1)
    
    def language(self) -> str:
        return self.repo_data.get("language", "get_language_failed")
    
    def has(self, feature: str) -> bool:
        """feature options: 'issues', 'projects', 'downloads', 'wiki', 'pages', 'discussions'"""
        return self.repo_data.get(f"has_{feature}", False)

    def forks_count(self) -> int:
        return self.repo_data.get("forks_count", -1)
    
    def is_archived(self) -> bool:
        return self.repo_data.get("archived", False)
    
    def is_disabled(self) -> bool:
        return self.repo_data.get("disabled", False)
    
    def open_issues_count(self) -> int:
        return self.repo_data.get("open_issues_count", -1)
    
    def license(self) -> dict | None:
        return self.repo_data.get("license", None)
    
    def allow_forking(self) -> bool:
        return self.repo_data.get("allow_forking", False)
    
    def is_template(self) -> bool:
        return self.repo_data.get("is_template", False)
    
    def web_commit_signoff_required(self) -> bool:
        return self.repo_data.get("web_commit_signoff_required", False)
    
    def topics(self) -> list[str]:
        return self.repo_data.get("topics", ["get_topics_failed"])
    
    def visibility(self) -> str:
        return self.repo_data.get("visibility", "get_visibility_failed")
    
    def forks(self) -> int:
        return self.repo_data.get("forks", -1)
    
    def open_issues(self) -> int:
        return self.repo_data.get("open_issues", -1)
    
    def watchers(self) -> int:
        return self.repo_data.get("watchers", -1)
    
    def default_branch(self) -> str:
        return self.repo_data.get("default_branch", "get_default_branch_failed")
    
    def permissions(self, permission: str = '') -> dict | bool:
        """permission options: None (returns 'permissions'), 'admin', 'maintain', 'push', 'triage', 'pull'"""
        permissions = self.repo_data.get("permissions", {"get_permissions_failed": True})
        if permission == '':
            return permissions
        return permissions.get(permission, False)