import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { WorkflowSseService, WorkflowEvent } from '../../../core/services/workflow-sse.service';

interface AgentState {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  message: string;
}

@Component({
  selector: 'app-workflow-progress',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './workflow-progress.component.html',
  styleUrls: ['./workflow-progress.component.css']
})
export class WorkflowProgressComponent implements OnInit, OnDestroy {
  @Input() tripId!: string;
  
  public agents: AgentState[] = [];
  public checkpointRequired = false;
  public checkpointData: any = null;
  public workflowCompleted = false;

  private sseSub?: Subscription;

  constructor(private sseService: WorkflowSseService) {}

  ngOnInit(): void {
    if (this.tripId) {
      this.sseSub = this.sseService.connect(this.tripId).subscribe(event => {
        this.handleEvent(event);
      });
    }
  }

  ngOnDestroy(): void {
    if (this.sseSub) {
      this.sseSub.unsubscribe();
    }
    this.sseService.disconnect();
  }

  private handleEvent(event: WorkflowEvent): void {
    if (event.type === 'checkpoint_required') {
      this.checkpointRequired = true;
      this.checkpointData = event.data;
      return;
    }
    if (event.type === 'workflow_completed') {
      this.workflowCompleted = true;
      return;
    }

    if (event.agent_name) {
      let agent = this.agents.find(a => a.name === event.agent_name);
      if (!agent) {
        agent = { name: event.agent_name, status: 'pending', message: event.message };
        this.agents.push(agent);
      }

      if (event.type === 'agent_started') {
        agent.status = 'running';
        agent.message = event.message;
      } else if (event.type === 'agent_completed') {
        agent.status = 'completed';
        agent.message = event.message;
      } else if (event.type === 'agent_failed') {
        agent.status = 'failed';
        agent.message = event.message;
      }
    }
  }
}
