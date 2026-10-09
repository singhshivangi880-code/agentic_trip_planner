import { ComponentFixture, TestBed } from '@angular/core/testing';
import { WorkflowProgressComponent } from './workflow-progress.component';
import { WorkflowSseService, WorkflowEvent } from '../../../core/services/workflow-sse.service';
import { Subject } from 'rxjs';

class MockWorkflowSseService {
  public eventSubject = new Subject<WorkflowEvent>();
  connect(tripId: string) {
    return this.eventSubject.asObservable();
  }
  disconnect() {}
}

describe('WorkflowProgressComponent', () => {
  let component: WorkflowProgressComponent;
  let fixture: ComponentFixture<WorkflowProgressComponent>;
  let mockService: MockWorkflowSseService;

  beforeEach(async () => {
    mockService = new MockWorkflowSseService();
    
    await TestBed.configureTestingModule({
      imports: [WorkflowProgressComponent],
      providers: [
        { provide: WorkflowSseService, useValue: mockService }
      ]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WorkflowProgressComponent);
    component = fixture.componentInstance;
    component.tripId = '123';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should add agent and set status to running', () => {
    mockService.eventSubject.next({
      type: 'agent_started',
      agent_name: 'TestAgent',
      message: 'Agent started'
    });
    
    expect(component.agents.length).toBe(1);
    expect(component.agents[0].name).toBe('TestAgent');
    expect(component.agents[0].status).toBe('running');
  });

  it('should show checkpoint when required', () => {
    mockService.eventSubject.next({
      type: 'checkpoint_required',
      message: 'Decision needed',
      data: { question: 'What to do?', options: ['A', 'B'] }
    });
    
    expect(component.checkpointRequired).toBeTrue();
    expect(component.checkpointData.question).toBe('What to do?');
  });
});
