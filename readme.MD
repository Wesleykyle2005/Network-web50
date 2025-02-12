# Network

Esta es la solución al proyecto **Network** del curso *CS50’s Web Programming with Python and JavaScript* de Harvard.

## Descripción

La aplicación es una red social básica que permite a los usuarios:
  
- **Realizar nuevos posts:** Los usuarios autenticados pueden crear publicaciones de texto mediante un formulario o modal.
- **Ver todas las publicaciones:** Se muestra una lista de todas las publicaciones de todos los usuarios en orden descendente (de más reciente a más antiguo), con paginación (10 posts por página).
- **Perfil de usuario:** Al hacer click en el nombre de usuario se carga la página de perfil, donde se visualiza la biografía del usuario, su avatar, la cantidad de seguidores y de personas a quienes sigue, y se listan sus publicaciones.
- **Seguir/Dejar de seguir:** En la página de perfil, los usuarios autenticados pueden seguir o dejar de seguir a otros usuarios (no se permite seguir a uno mismo).
- **Ver publicaciones de quienes se sigue:** La vista “Following” muestra sólo los posts de los usuarios a los que el usuario actual está siguiendo.
- **Editar publicaciones:** Los usuarios pueden editar sus propias publicaciones a través de un modal que les permite modificar el contenido. La edición se realiza de forma asíncrona (similar a la funcionalidad de “like” o “follow”) sin recargar la página.
- **Dar “Like” a las publicaciones:** Los usuarios pueden dar “like” o quitar “like” a cualquier publicación. La acción se realiza de forma asíncrona con actualización en el DOM sin recarga de página.

## Tecnologías utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **AJAX (fetch):** Para la actualización asíncrona de “likes”, edición de posts y otras interacciones.
- **Base de datos:** Utilizada a través de Django ORM (SQLite en desarrollo).

## Estructura del proyecto

- **Templates:** Las plantillas HTML se encuentran distribuidas en el directorio `network/templates/network/` y definen las vistas para el feed de posts, perfil de usuario, seguimiento de usuarios, y modales para crear o editar publicaciones.
- **Archivos estáticos:** El JavaScript (como `script.js`) y CSS personalizados se encuentran en `network/static/network/`.
- **Vistas y URLs:** La lógica de manejo de solicitudes, incluyendo la creación, edición, “like” y “follow”, se define en las vistas de Django y se rastrean mediante el archivo `urls.py`.

## Funcionalidades clave

- **New Post:** Permite la creación de nuevos posts mediante un formulario/modal.
- **All Posts & Pagination:** Muestra todos los posts con paginación y permite navegar entre páginas.
- **Profile Page:** Muestra la información del usuario, sus seguidores, seguidos y publicaciones.
- **Following:** Muestra los posts de los usuarios que el usuario actual sigue.
- **Edit Post:** Los usuarios pueden editar sus propias publicaciones sin recargar la página.
- **“Like” and “Unlike”:** Los usuarios pueden alternar “likes” en cada publicación, actualizando asíncronamente el DOM.
