<h2><strong>Luis Angelo Hernandez Centti</strong></h2>

# Blue-Green Deployment Workflow

## Initial Deployment

When you deploy the Terraform configuration for the first time:

1. **Blue Environment Setup**: The ECS service starts with the **blue target group** (`app_tg_blue`)
2. **Load Balancer Configuration**: 
   - Port 80 listener → Routes traffic to blue target group (production traffic)
   - Port 8080 listener → Routes traffic to green target group (test traffic)
3. **Initial State**: The application runs in the blue environment and receives all production traffic

## Blue-Green Switch Trigger

The blue-green deployment is **automatically triggered** when:

### ✅ **Automatic Triggers**
- **New commit to main branch** in the GitHub repository (`luhercentti/awsdevopsstackdemo`)
- **Any code changes** pushed to the configured branch

### 🔄 **Pipeline Execution Flow**

1. **Source Stage**: CodePipeline detects changes in GitHub (via CodeStar connection)
2. **Build Stage**: CodeBuild builds new Docker image and pushes to ECR
3. **Deploy Stage**: CodeDeploy performs blue-green deployment

## Blue-Green Deployment Process

### Phase 1: Green Environment Preparation
```
Current State: Blue (Production) ← All traffic
Target State:  Green (Staging) ← New version deployed
```

1. **New Task Definition**: CodeDeploy creates new ECS task definition with updated image
2. **Green Deployment**: New version deploys to green target group
3. **Health Checks**: Load balancer performs health checks on green environment

### Phase 2: Traffic Switching
```
Before: Port 80 → Blue (100% traffic)
        Port 8080 → Green (test traffic)

After:  Port 80 → Green (100% traffic) 
        Port 8080 → Blue (test traffic)
```

4. **Automatic Switch**: If health checks pass, traffic switches from blue to green
5. **Blue Termination**: Old blue environment terminates after 1 minute (configured in this setup)

## Key Configuration Details

### CodeDeploy Configuration
```hcl
deployment_config_name = "CodeDeployDefault.ECSAllAtOnce"
```
- **All-at-once deployment**: Traffic switches completely from blue to green

### Auto-Rollback
```hcl
auto_rollback_configuration {
  enabled = true
  events  = ["DEPLOYMENT_FAILURE"]
}
```
- **Automatic rollback** if deployment fails

### Termination Settings
```hcl
terminate_blue_instances_on_deployment_success {
  action                           = "TERMINATE"
  termination_wait_time_in_minutes = 1
}
```
- **1-minute wait** before terminating old version

### Traffic Control
```hcl
deployment_style {
  deployment_option = "WITH_TRAFFIC_CONTROL"
  deployment_type   = "BLUE_GREEN"
}
```
- **Controlled traffic switching** between environments

## Monitoring the Process

### 1. **AWS CodePipeline Console**
- View pipeline execution status
- Track each stage (Source → Build → Deploy)

### 2. **AWS CodeDeploy Console**
- Monitor blue-green deployment progress
- View traffic shifting status

### 3. **Load Balancer Health Checks**
- **Health check path**: `/health`
- **Success criteria**: HTTP 200 response
- **Check interval**: 30 seconds

### 4. **ECS Service Console**
- View running tasks in both environments
- Monitor service events and deployment status

## Testing Strategy

### Production Testing (Port 80)
```bash
curl http://your-load-balancer-dns-name/
```

### Staging/Test Environment (Port 8080)
```bash
curl http://your-load-balancer-dns-name:8080/
```

## Timeline Example

```
T+0min:  New commit pushed to GitHub
T+1min:  CodePipeline triggered, source stage completes
T+3min:  CodeBuild starts building Docker image
T+8min:  Image pushed to ECR, CodeDeploy starts
T+10min: Green environment receives new deployment
T+12min: Health checks pass, traffic switches to green
T+13min: Blue environment terminates
T+13min: Deployment complete ✅
```

## Important Notes

### ⚠️ **First Deployment Behavior**
- Initial deployment goes to **blue environment**
- **Second deployment** triggers first blue-green switch

### 🔄 **Subsequent Deployments**
- Each new commit alternates between blue and green
- Previous environment becomes the new staging environment

### 🛡️ **Rollback Strategy**
- Automatic rollback on deployment failure
- Manual rollback available through CodeDeploy console
- Previous version always maintained until new deployment succeeds

### 📊 **Health Check Requirements**
The application exposes a /health endpoint that returns HTTP 200 for successful deployments.
**Application**:
   - The simple Flask application exposes two endpoints:
     - `/`: Returns a JSON response with a greeting message
     - `/health`: Returns the health status

## Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── buildspec.yml           # AWS CodeBuild configuration
├── appspec.yml             # AWS CodeDeploy configuration
└── README.md               # This file
```

/////
Infracost analysis:

terraform show -json tfplan.binary > tfplan.json
infracost breakdown --path=tfplan.json


<h3><strong>Luis Angelo Hernandez Centti</strong></h3>
