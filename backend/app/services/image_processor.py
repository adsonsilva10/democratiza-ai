"""
Serviço de processamento de imagens para otimização de OCR
Aplica filtros e correções automaticamente para melhorar a legibilidade
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Tuple, Optional, List
import base64
from dataclasses import dataclass

@dataclass
class ImageProcessingResult:
    enhanced_image: np.ndarray
    original_size: Tuple[int, int]
    enhanced_size: Tuple[int, int]
    confidence_score: float
    applied_filters: List[str]

class DocumentImageProcessor:
    """Processador de imagens especializado para documentos"""
    
    def __init__(self):
        self.min_confidence = 0.7
        self.target_dpi = 300
        self.max_dimension = 2048
        
    def process_document_image(
        self, 
        image_data: bytes,
        auto_enhance: bool = True,
        preserve_colors: bool = False
    ) -> ImageProcessingResult:
        """
        Processa uma imagem de documento para otimizar OCR
        
        Args:
            image_data: Dados binários da imagem
            auto_enhance: Se deve aplicar melhorias automáticas
            preserve_colors: Se deve preservar cores originais
            
        Returns:
            ImageProcessingResult com imagem otimizada
        """
        # Converter para OpenCV
        image = self._bytes_to_opencv(image_data)
        original_size = image.shape[:2]
        
        applied_filters = []
        confidence_score = 0.0
        
        # Pipeline de processamento
        if auto_enhance:
            # 1. Correção de perspectiva
            image, perspective_applied = self._correct_perspective(image)
            if perspective_applied:
                applied_filters.append("perspective_correction")
                
            # 2. Redimensionamento inteligente
            image = self._smart_resize(image)
            applied_filters.append("smart_resize")
            
            # 3. Redução de ruído
            image = self._reduce_noise(image)
            applied_filters.append("noise_reduction")
            
            # 4. Melhoria de contraste
            image = self._enhance_contrast(image)
            applied_filters.append("contrast_enhancement")
            
            # 5. Correção de iluminação
            image = self._correct_lighting(image)
            applied_filters.append("lighting_correction")
            
            # 6. Nitidez adaptativa
            image = self._adaptive_sharpening(image)
            applied_filters.append("adaptive_sharpening")
            
            if not preserve_colors:
                # 7. Binarização inteligente
                image = self._intelligent_binarization(image)
                applied_filters.append("binarization")
        
        # Calcular score de confiança
        confidence_score = self._calculate_confidence_score(image)
        
        enhanced_size = image.shape[:2]
        
        return ImageProcessingResult(
            enhanced_image=image,
            original_size=original_size,
            enhanced_size=enhanced_size,
            confidence_score=confidence_score,
            applied_filters=applied_filters
        )
    
    def _bytes_to_opencv(self, image_data: bytes) -> np.ndarray:
        """Converte bytes para imagem OpenCV"""
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
    
    def _opencv_to_bytes(self, image: np.ndarray, format: str = 'PNG') -> bytes:
        """Converte imagem OpenCV para bytes"""
        is_success, buffer = cv2.imencode(f'.{format.lower()}', image)
        if is_success:
            return buffer.tobytes()
        raise ValueError("Erro ao codificar imagem")
    
    def _correct_perspective(self, image: np.ndarray) -> Tuple[np.ndarray, bool]:
        """Corrige perspectiva do documento usando detecção de bordas"""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detecção de bordas
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Encontrar o maior contorno retangular
            for contour in sorted(contours, key=cv2.contourArea, reverse=True):
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:
                    # Ordenar pontos
                    pts = approx.reshape(4, 2)
                    rect = self._order_points(pts)
                    
                    # Calcular dimensões do retângulo de destino
                    (tl, tr, br, bl) = rect
                    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                    maxWidth = max(int(widthA), int(widthB))
                    
                    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                    maxHeight = max(int(heightA), int(heightB))
                    
                    # Pontos de destino
                    dst = np.array([
                        [0, 0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1],
                        [0, maxHeight - 1]], dtype="float32")
                    
                    # Aplicar transformação de perspectiva
                    M = cv2.getPerspectiveTransform(rect, dst)
                    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
                    
                    return warped, True
            
            return image, False
            
        except Exception:
            return image, False
    
    def _order_points(self, pts: np.ndarray) -> np.ndarray:
        """Ordena pontos em ordem: top-left, top-right, bottom-right, bottom-left"""
        rect = np.zeros((4, 2), dtype="float32")
        
        # Top-left: menor soma
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        
        # Bottom-right: maior soma
        rect[2] = pts[np.argmax(s)]
        
        # Top-right: menor diferença
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        
        # Bottom-left: maior diferença
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def _smart_resize(self, image: np.ndarray) -> np.ndarray:
        """Redimensiona mantendo proporção e otimizando para OCR"""
        height, width = image.shape[:2]
        
        # Se já está em bom tamanho, não redimensionar
        if max(height, width) <= self.max_dimension:
            return image
            
        # Calcular nova escala
        scale = self.max_dimension / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Redimensionar com interpolação de alta qualidade
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        return resized
    
    def _reduce_noise(self, image: np.ndarray) -> np.ndarray:
        """Aplica filtros de redução de ruído preservando texto"""
        # Filtro bilateral: remove ruído preservando bordas
        denoised = cv2.bilateralFilter(image, 9, 75, 75)
        
        return denoised
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Melhora contraste usando CLAHE adaptativo"""
        # Converter para LAB
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Aplicar CLAHE apenas no canal L (luminância)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Recombinar canais
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def _correct_lighting(self, image: np.ndarray) -> np.ndarray:
        """Corrige iluminação desigual"""
        # Converter para cinza para análise
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Criar máscara de iluminação usando filtro gaussiano
        blur = cv2.GaussianBlur(gray, (0, 0), sigmaX=gray.shape[1]/30)
        
        # Normalizar iluminação
        normalized = cv2.divide(gray, blur, scale=255)
        
        # Aplicar correção aos canais de cor
        corrected = image.copy()
        for i in range(3):
            corrected[:, :, i] = cv2.multiply(
                corrected[:, :, i], 
                normalized, 
                scale=1/255
            )
        
        return corrected
    
    def _adaptive_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Aplica nitidez adaptativa"""
        # Kernel de nitidez
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        
        # Aplicar com peso adaptativo
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Combinar com original (50% cada)
        result = cv2.addWeighted(image, 0.5, sharpened, 0.5, 0)
        
        return result
    
    def _intelligent_binarization(self, image: np.ndarray) -> np.ndarray:
        """Binarização adaptativa inteligente"""
        # Converter para cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Binarização adaptativa Gaussiana
        binary = cv2.adaptiveThreshold(
            gray, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 
            2
        )
        
        # Converter de volta para BGR para compatibilidade
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        return result
    
    def _calculate_confidence_score(self, image: np.ndarray) -> float:
        """Calcula score de confiança baseado na qualidade da imagem"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Nitidez (variância do Laplaciano)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 1000, 1.0)
        
        # 2. Contraste (desvio padrão)
        contrast_score = min(gray.std() / 128, 1.0)
        
        # 3. Uniformidade da iluminação
        mean_brightness = gray.mean()
        brightness_score = 1.0 - abs(mean_brightness - 127) / 127
        
        # Score final ponderado
        final_score = (
            sharpness_score * 0.4 +
            contrast_score * 0.4 +
            brightness_score * 0.2
        )
        
        return min(final_score, 1.0)
    
    def process_multiple_pages(
        self, 
        images_data: List[bytes],
        auto_enhance: bool = True
    ) -> List[ImageProcessingResult]:
        """Processa múltiplas páginas mantendo consistência"""
        results = []
        
        for image_data in images_data:
            result = self.process_document_image(
                image_data=image_data,
                auto_enhance=auto_enhance
            )
            results.append(result)
        
        return results
    
    def get_enhanced_image_bytes(
        self, 
        result: ImageProcessingResult, 
        format: str = 'PNG'
    ) -> bytes:
        """Retorna imagem processada como bytes"""
        return self._opencv_to_bytes(result.enhanced_image, format)