import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { WorkflowSseService, WorkflowEvent } from '../../../core/services/workflow-sse.service';
import { TripApiService } from '../../../core/services/trip_api.service';

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
  @Output() completed = new EventEmitter<void>();
  @Output() viewItinerary = new EventEmitter<void>();
  @Output() decisionMade = new EventEmitter<string>();
  
  private tripApi = inject(TripApiService);
  private sseService = inject(WorkflowSseService);

  public agents: AgentState[] = [];
  public checkpointRequired = false;
  public checkpointData: any = null;
  public selectedDecision: string | null = null;
  public workflowCompleted = false;

  private sseSub?: Subscription;

  ngOnInit(): void {
    if (this.tripId) {
      this.connect();
    }
  }

  ngOnDestroy(): void {
    this.disconnect();
  }

  public connect(): void {
    this.disconnect();
    this.agents = [];
    this.workflowCompleted = false;
    this.checkpointRequired = false;
    this.selectedDecision = null;

    this.sseSub = this.sseService.connect(this.tripId).subscribe(event => {
      this.handleEvent(event);
    });
  }

  public disconnect(): void {
    if (this.sseSub) {
      this.sseSub.unsubscribe();
      this.sseSub = undefined;
    }
    this.sseService.disconnect();
  }

  public onSelectOption(option: string): void {
    this.selectedDecision = option;
    this.checkpointRequired = false;
    this.decisionMade.emit(option);
    const decisionId = this.checkpointData?.decision_id || 'checkpoint_1';
    
    this.tripApi.submitDecision(this.tripId, {
      decision_id: decisionId,
      selected_option: option
    }).subscribe({
      next: () => {},
      error: (err) => console.error('Error submitting decision:', err)
    });

    this.viewItinerary.emit();
  }

  private handleEvent(event: WorkflowEvent): void {
    if (event.type === 'checkpoint_required') {
      this.checkpointRequired = true;
      this.checkpointData = event.data;
      return;
    }
    if (event.type === 'workflow_completed') {
      this.workflowCompleted = true;
      this.checkpointRequired = false;
      this.completed.emit();
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
