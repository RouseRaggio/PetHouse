import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminNavbarComponent } from '../../../../shared/components/admin-navbar/admin-navbar';
import { AiAssistantService } from '../../services/ai-assistant.service';
import { HistoryItem } from './ai.models';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  sql?: string | null;
  executionTime?: number | null;
  provider?: string;
  model?: string;
  timestamp: Date;
}

@Component({
  selector: 'app-ai-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule, AdminNavbarComponent],
  templateUrl: './ai-assistant.component.html',
  styleUrls: ['./ai-assistant.component.css'],
})
export class AiAssistantComponent implements OnInit {
  messages: ChatMessage[] = [];
  question = '';
  loading = false;
  history: HistoryItem[] = [];
  showHistory = true;
  error = '';
  copiedIndex: number | null = null;

  constructor(private aiService: AiAssistantService) {}

  ngOnInit(): void {
    this.loadHistory();
    this.messages.push({
      role: 'assistant',
      content:
        '¡Hola! Soy tu asistente SQL para el panel de administración. Puedes preguntarme sobre los datos de PetHouse en lenguaje natural y te ayudaré a generar consultas SQL.',
      timestamp: new Date(),
    });
  }

  async send(): Promise<void> {
    const q = this.question.trim();
    if (!q || this.loading) return;

    this.messages.push({ role: 'user', content: q, timestamp: new Date() });
    this.question = '';
    this.loading = true;
    this.error = '';

    try {
      const response = await this.aiService.ask(q);
      this.messages.push({
        role: 'assistant',
        content: response.answer,
        sql: response.generated_sql,
        executionTime: response.execution_time_ms,
        provider: response.provider,
        model: response.model,
        timestamp: new Date(),
      });
      await this.loadHistory();
    } catch (err: any) {
      this.error =
        err.error?.detail || 'Ocurrió un error al procesar tu solicitud.';
    } finally {
      this.loading = false;
    }
  }

  async loadHistory(): Promise<void> {
    try {
      this.history = await this.aiService.getHistory();
    } catch {
      // Silently fail
    }
  }

  selectHistoryItem(item: HistoryItem): void {
    this.messages.push({
      role: 'user',
      content: item.question,
      timestamp: new Date(),
    });
    this.messages.push({
      role: 'assistant',
      content: item.answer,
      sql: item.generated_sql,
      executionTime: item.execution_time_ms,
      provider: item.provider,
      timestamp: new Date(),
    });
  }

  clearChat(): void {
    this.messages = [];
    this.error = '';
    this.messages.push({
      role: 'assistant',
      content:
        '¡Hola! Soy tu asistente SQL para el panel de administración. Puedes preguntarme sobre los datos de PetHouse en lenguaje natural y te ayudaré a generar consultas SQL.',
      timestamp: new Date(),
    });
  }

  async copySql(sql: string, index: number): Promise<void> {
    try {
      await navigator.clipboard.writeText(sql);
      this.copiedIndex = index;
      setTimeout(() => (this.copiedIndex = null), 2000);
    } catch {
      // Clipboard not available
    }
  }
}
