# Performance Code Review Template

## Algorithmic Efficiency
- [ ] Algorithms have appropriate time complexity for the task
- [ ] Data structures are optimal for the operations performed
- [ ] No unnecessary iterations or nested loops
- [ ] Sorting and searching operations use efficient methods

## Resource Management
- [ ] Memory usage is optimized
- [ ] Resources are properly released when no longer needed
- [ ] No memory leaks
- [ ] Proper caching strategy is implemented

## Database Interactions
- [ ] Database queries are optimized
- [ ] Appropriate indexes are utilized
- [ ] Batch operations used when applicable
- [ ] Connection pooling is properly configured
- [ ] N+1 query problems are avoided

## Concurrency & Parallelism
- [ ] Thread safety is ensured where needed
- [ ] Parallel processing is used appropriately
- [ ] Race conditions are prevented
- [ ] Deadlocks are avoided

## Network Efficiency
- [ ] API calls are minimized
- [ ] Data payloads are appropriate in size
- [ ] Proper use of lazy loading
- [ ] Network resources are used efficiently

## CPU & Processing
- [ ] CPU-intensive operations are optimized
- [ ] Calculations are simplified where possible
- [ ] Heavy processing is done in the background when appropriate
- [ ] Computations are cached where applicable

## Frontend Performance (if applicable)
- [ ] Assets are properly optimized
- [ ] Rendering performance is considered
- [ ] JavaScript execution is efficient
- [ ] DOM manipulations are minimized

## Performance Testing & Metrics
- [ ] Performance tests exist for critical paths
- [ ] Baselines and thresholds are defined
- [ ] Monitoring points are established
- [ ] Performance metrics are recorded and analyzed

## Additional Performance Concerns
- Add any specific performance feedback or concerns here