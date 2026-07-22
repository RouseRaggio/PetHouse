import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { AskRequest, AskResponse, HistoryItem } from '../pages/ai-assistant/ai.models';

@Injectable({ providedIn: 'root' })
export class AiAssistantService {
  private apiUrl = 'http://localhost:8000/api/v1/ai';

  constructor(private http: HttpClient) {}

  async ask(question: string): Promise<AskResponse> {
    const body: AskRequest = { question };
    return firstValueFrom(
      this.http.post<AskResponse>(`${this.apiUrl}/ask`, body),
    );
  }

  async getHistory(): Promise<HistoryItem[]> {
    return firstValueFrom(
      this.http.get<HistoryItem[]>(`${this.apiUrl}/history`),
    );
  }
}
