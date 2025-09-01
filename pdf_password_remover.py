#!/bin/bash
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font
import os
import threading

###############################################################################
############################ Password PDF Remover #############################
###############################################################################

try:
    import pikepdf
    PDF_LIBRARY = "pikepdf"
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = "PyPDF2"
    except ImportError:
        PDF_LIBRARY = None

class PDFPasswordRemover:
    def __init__(self, root):
        self.root = root
        self.root.title("Removedor de Contraseñas PDF")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.pdf_path = tk.StringVar()
        self.password = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.create_widgets()
        self.check_dependencies()
    
    def check_dependencies(self):
        if PDF_LIBRARY is None:
            messagebox.showerror(
                "Error de dependencias",
                "No se encontraron las librerías necesarias.\n\n"
                "Por favor instala una de estas librerías:\n"
                "• pip install pikepdf\n"
                "• pip install PyPDF2"
            )
            self.process_button.config(state='disabled')
    
    def create_widgets(self):
        # Título
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(
            self.root, 
            text="Removedor de Contraseñas PDF", 
            font=title_font,
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Selección de archivo PDF
        pdf_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pdf_frame.pack(fill='x', pady=10)
        
        tk.Label(
            pdf_frame, 
            text="Archivo PDF:", 
            bg='#f0f0f0',
            font=('Arial', 10, 'bold')
        ).pack(anchor='w')
        
        pdf_input_frame = tk.Frame(pdf_frame, bg='#f0f0f0')
        pdf_input_frame.pack(fill='x', pady=(5, 0))
        
        self.pdf_entry = tk.Entry(
            pdf_input_frame, 
            textvariable=self.pdf_path,
            state='readonly',
            bg='white',
            relief='sunken',
            bd=1
        )
        self.pdf_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_button = tk.Button(
            pdf_input_frame,
            text="Examinar",
            command=self.browse_pdf,
            bg='#4CAF50',
            fg='white',
            relief='raised',
            bd=1,
            padx=20
        )
        browse_button.pack(side='right')
        
        # Campo de contraseña
        password_frame = tk.Frame(main_frame, bg='#f0f0f0')
        password_frame.pack(fill='x', pady=10)
        
        tk.Label(
            password_frame, 
            text="Contraseña del PDF:", 
            bg='#f0f0f0',
            font=('Arial', 10, 'bold')
        ).pack(anchor='w')
        
        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password,
            show="*",
            bg='white',
            relief='sunken',
            bd=1
        )
        self.password_entry.pack(fill='x', pady=(5, 0))
        
        # Selección de archivo de salida
        output_frame = tk.Frame(main_frame, bg='#f0f0f0')
        output_frame.pack(fill='x', pady=10)
        
        tk.Label(
            output_frame, 
            text="Guardar como:", 
            bg='#f0f0f0',
            font=('Arial', 10, 'bold')
        ).pack(anchor='w')
        
        output_input_frame = tk.Frame(output_frame, bg='#f0f0f0')
        output_input_frame.pack(fill='x', pady=(5, 0))
        
        self.output_entry = tk.Entry(
            output_input_frame,
            textvariable=self.output_path,
            bg='white',
            relief='sunken',
            bd=1
        )
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        save_as_button = tk.Button(
            output_input_frame,
            text="Guardar como",
            command=self.browse_output,
            bg='#2196F3',
            fg='white',
            relief='raised',
            bd=1,
            padx=20
        )
        save_as_button.pack(side='right')
        
        # Botón de procesar
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=20)
        
        self.process_button = tk.Button(
            button_frame,
            text="Remover Contraseña",
            command=self.process_pdf_threaded,
            bg='#FF9800',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            bd=2,
            padx=30,
            pady=10
        )
        self.process_button.pack()
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)
        
        # Área de estado
        self.status_label = tk.Label(
            main_frame,
            text="Selecciona un archivo PDF para comenzar",
            bg='#f0f0f0',
            fg='#666666',
            font=('Arial', 9)
        )
        self.status_label.pack(pady=10)
        
        # Información de la librería
        if PDF_LIBRARY:
            info_text = f"Usando librería: {PDF_LIBRARY}"
        else:
            info_text = "¡Falta instalar librería PDF!"
            
        info_label = tk.Label(
            main_frame,
            text=info_text,
            bg='#f0f0f0',
            fg='#888888',
            font=('Arial', 8)
        )
        info_label.pack(side='bottom', pady=(20, 0))
    
    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            # Sugerir nombre de salida
            base_name = os.path.splitext(filename)[0]
            suggested_output = f"{base_name}_sin_clave.pdf"
            self.output_path.set(suggested_output)
            self.status_label.config(text="Archivo PDF seleccionado")
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Guardar PDF sin contraseña",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def process_pdf_threaded(self):
        """Ejecutar el procesamiento en un hilo separado para no bloquear la UI"""
        thread = threading.Thread(target=self.process_pdf)
        thread.daemon = True
        thread.start()
    
    def process_pdf(self):
        # Validaciones
        if not self.pdf_path.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo PDF")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Por favor ingresa la contraseña del PDF")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Por favor especifica dónde guardar el archivo")
            return
        
        # Inicio de progreso
        self.progress.start()
        self.process_button.config(state='disabled')
        self.status_label.config(text="Procesando PDF...")
        self.root.update()
        
        try:
            if PDF_LIBRARY == "pikepdf":
                self.remove_password_pikepdf()
            elif PDF_LIBRARY == "PyPDF2":
                self.remove_password_pypdf2()
            else:
                raise Exception("No hay librería PDF disponible")
            
            self.status_label.config(text="¡PDF procesado exitosamente!")
            messagebox.showinfo(
                "Éxito", 
                f"El PDF sin contraseña se guardó en:\n{self.output_path.get()}"
            )
            
        except Exception as e:
            self.status_label.config(text="Error al procesar el PDF")
            messagebox.showerror("Error", f"Error al procesar el PDF:\n{str(e)}")
        
        finally:
            self.progress.stop()
            self.process_button.config(state='normal')
    
    def remove_password_pikepdf(self):
        """Remover contraseña usando pikepdf"""
        with pikepdf.open(
            self.pdf_path.get(), 
            password=self.password.get()
        ) as pdf:
            pdf.save(self.output_path.get())
    
    def remove_password_pypdf2(self):
        """Remover la contraseña usando PyPDF2"""
        with open(self.pdf_path.get(), 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            
            if reader.is_encrypted:
                reader.decrypt(self.password.get())
            
            writer = PyPDF2.PdfWriter()
            
            for page in reader.pages:
                writer.add_page(page)
            
            with open(self.output_path.get(), 'wb') as output_file:
                writer.write(output_file)

def main():
    root = tk.Tk()
    app = PDFPasswordRemover(root)
    root.mainloop()

if __name__ == "__main__":
    main()