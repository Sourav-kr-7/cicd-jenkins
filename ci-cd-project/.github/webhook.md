## GitHub Webhook → Jenkins (Real-time trigger)

### 1) Jenkins prerequisites
- Install plugins:
  - **Git**
  - **GitHub**
  - **Pipeline**
- Create a Pipeline job.
- In the job configuration:
  - **Pipeline definition**: *Pipeline script from SCM*
  - **SCM**: *Git*
  - **Repository URL**: your repo URL
  - **Script Path**: `jenkins/Jenkinsfile`
  - **Build Triggers**: enable **GitHub hook trigger for GITScm polling**

### 2) GitHub webhook setup
- In GitHub repo: **Settings → Webhooks → Add webhook**
- **Payload URL**: `http(s)://<your-jenkins-host>/github-webhook/`
- **Content type**: `application/json`
- **Which events**: `Just the push event`
- Save.

### 3) Validate
- Push a commit to your repo and confirm Jenkins builds automatically.

