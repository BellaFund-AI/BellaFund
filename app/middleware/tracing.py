async def tracing_middleware(request: Request, call_next):
    """FastAPI middleware for distributed tracing"""
    tracer = request.app.state.tracer
    headers = request.headers
    
    # Extract tracing context from headers
    parent_ctx = None
    if 'x-trace-id' in headers:
        parent_ctx = {
            'trace_id': headers['x-trace-id'],
            'span_id': headers['x-span-id']
        }
    
    # Start request span
    span = tracer.start_span(
        name=f"{request.method} {request.url.path}",
        parent_id=f"{parent_ctx['trace_id']}:{parent_ctx['span_id']}" if parent_ctx else None
    )
    
    # Propagate tracing headers
    request.state.trace_id = span['trace_id']
    request.state.span_id = span['span_id']
    
    try:
        response = await call_next(request)
    except Exception as e:
        tracer.add_tag('error', str(e))
        raise
    finally:
        tracer.end_span()
        # Log span to collector
        tracing_collector.log_span(span)
    
    # Inject tracing headers in response
    response.headers['x-trace-id'] = span['trace_id']
    response.headers['x-span-id'] = span['span_id']
    return response 