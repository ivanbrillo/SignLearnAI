import customtkinter as ctk
import matplotlib

from config import FONT_FAMILY, errors, ASL_CLASS_NAMES

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HomeScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.app = master
        self._build_ui()

    def _build_ui(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Welcome to ASL Quiz Game!",
            font=(FONT_FAMILY, 28, "bold")
        )
        title_label.pack(pady=30)

        # Instructions
        instruction_label = ctk.CTkLabel(
            self,
            text="Choose a learning mode below:",
            font=(FONT_FAMILY, 18)
        )
        instruction_label.pack(pady=10)

        # Mode selection frame
        modes_frame = ctk.CTkFrame(self, fg_color="transparent")
        modes_frame.pack(pady=10)

        # Letter quiz section
        quiz_label = ctk.CTkLabel(
            modes_frame,
            text="Individual Letters Quiz",
            font=(FONT_FAMILY, 16, "bold")
        )
        quiz_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        # Easy mode button
        easy_button = ctk.CTkButton(
            modes_frame,
            text="Easy Mode",
            font=(FONT_FAMILY, 16),
            command=lambda: self.app.start_quiz("easy")
        )
        easy_button.grid(row=1, column=0, padx=10, pady=5)

        # Hard mode button
        hard_button = ctk.CTkButton(
            modes_frame,
            text="Hard Mode",
            font=(FONT_FAMILY, 16),
            command=lambda: self.app.start_quiz("hard")
        )
        hard_button.grid(row=1, column=1, padx=10, pady=5)

        # Phrase practice section
        phrase_label = ctk.CTkLabel(
            modes_frame,
            text="Phrase Practice",
            font=(FONT_FAMILY, 16, "bold")
        )
        phrase_label.grid(row=2, column=0, columnspan=2, pady=(20, 10))

        # Phrase practice button
        phrase_button = ctk.CTkButton(
            modes_frame,
            text="Start Phrase Practice",
            font=(FONT_FAMILY, 16),
            command=self.app.start_phrase_practice,
        )
        phrase_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Custom phrase frame
        custom_phrase_frame = ctk.CTkFrame(self, fg_color="transparent")
        custom_phrase_frame.pack(pady=10)

        # Custom phrase entry
        self.phrase_entry = ctk.CTkEntry(
            custom_phrase_frame,
            width=300,
            font=(FONT_FAMILY, 16),
            placeholder_text="Enter custom phrase (letters A-Z only)"
        )
        self.phrase_entry.grid(row=0, column=0, padx=10, pady=10)

        # Custom phrase button
        custom_phrase_button = ctk.CTkButton(
            custom_phrase_frame,
            text="Practice Custom Phrase",
            font=(FONT_FAMILY, 16),
            command=self._start_custom_phrase
        )
        custom_phrase_button.grid(row=0, column=1, padx=10, pady=10)

        # Statistics button
        stats_button = ctk.CTkButton(
            self,
            text="Show Statistics",
            font=(FONT_FAMILY, 16),
            command=self.show_statistics_popup
        )
        stats_button.pack(pady=20)

    def _start_custom_phrase(self):
        """Start practice with a custom phrase from entry"""
        phrase = self.phrase_entry.get().strip()
        if phrase:
            # Filter to ensure phrase only contains valid ASL letters
            valid_chars = set(ASL_CLASS_NAMES + [" "])
            phrase = "".join(c for c in phrase.upper() if c in valid_chars)
            if phrase:
                self.app.start_phrase_practice(phrase)

    def show_statistics_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Error Statistics")
        popup.geometry("750x650")
        popup.grab_set()

        title = ctk.CTkLabel(
            popup,
            text="Error Statistics per Letter",
            font=(FONT_FAMILY, 20, "bold")
        )
        title.pack(pady=10)

        # Prepare data for plotting
        letters = ASL_CLASS_NAMES
        video_errors = [errors['letters'][ltr]['video_errors'] for ltr in letters]
        text_errors = [errors['letters'][ltr]['text_errors'] for ltr in letters]

        # Use dark background for plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(11, 4.5), facecolor='#222222')
        fig.patch.set_facecolor('#222222')
        ax.set_facecolor('#222222')

        x = range(len(letters))
        ax.bar(x, video_errors, width=0.4, label='Video Errors', color='#4F8DFD', align='center')
        ax.bar(x, text_errors, width=0.4, label='Text Errors', color='#FFB347', align='edge')
        ax.set_xticks(x)
        ax.set_xticklabels(letters, color='white')
        ax.set_xlabel('Letter', color='white')
        ax.set_ylabel('Errors', color='white')
        ax.set_title('Errors per Letter', color='white')
        ax.legend(facecolor='#222222', edgecolor='white', labelcolor='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='x', colors='white')
        fig.tight_layout(pad=3.0)

        # Embed the plot in the popup with padding
        plot_frame = ctk.CTkFrame(popup, fg_color="transparent")
        plot_frame.pack(padx=20, pady=10, fill="both", expand=True)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

        # Totals
        totals = ctk.CTkLabel(
            popup,
            text=f"Total Video Errors: {errors['video_total_errors']:.2f}\n"
                 f"Total Text Errors: {errors['text_total_errors']:.2f}\n"
                 f"Video Tests: {errors['video_tests']}\n"
                 f"Text Tests: {errors['text_tests']}",
            font=(FONT_FAMILY, 14)
        )
        totals.pack(pady=10)
