import { TestBed } from '@angular/core/testing';

import { WorkflowSseService } from './workflow-sse.service';

describe('WorkflowSseService', () => {
  let service: WorkflowSseService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WorkflowSseService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
