import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ShareViewComponent } from './share-view.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';

describe('ShareViewComponent', () => {
  let component: ShareViewComponent;
  let fixture: ComponentFixture<ShareViewComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShareViewComponent, HttpClientTestingModule, RouterTestingModule],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: {
              paramMap: {
                get: () => 'test-token-123'
              }
            }
          }
        }
      ]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ShareViewComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create and load itinerary', () => {
    expect(component).toBeTruthy();
    
    const req = httpMock.expectOne('/api/v1/share/test-token-123');
    expect(req.request.method).toBe('GET');
    
    req.flush({
      days: []
    });
    
    expect(component.loading).toBeFalse();
    expect(component.itinerary?.days).toEqual([]);
  });

  it('should display error on 404', () => {
    const req = httpMock.expectOne('/api/v1/share/test-token-123');
    req.flush('Not Found', { status: 404, statusText: 'Not Found' });
    
    expect(component.loading).toBeFalse();
    expect(component.error).toBe('This share link is invalid or has been revoked.');
  });
});
