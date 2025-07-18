rm(list = ls())
true_beta = 2
true_gamma = 1
true_rho = 0.25
true_i0 = 0.01
true_rho = 0.25
true_N = 100

guess_beta = 1.8
guess_gamma = 1.1

complete_pars <- function(beta = guess_beta, gamma = guess_gamma, N = true_N, 
                          i0 = true_i0, rho = true_rho, duration = 20, dt = 1){
  pars = data.frame(beta = beta, gamma = gamma, N = N,
                    i0 = i0, rho = rho, duration = duration, dt = dt)
  return(pars)
}

run_SIR <- function(pars){
  beta = pars[['beta']]
  gamma = pars[['gamma']]
  N = pars[['N']]
  i0 = pars[['i0']]
  rho = pars[['rho']]
  dt = pars[['dt']]
  duration = pars[['duration']]
  dt = pars[['dt']]
  times = seq(0,duration, by = dt)
  SIR_df = data.frame(time = times, 
                      S = 0, I = 0, R = 0, newI = 0, newC = 0)
  SIR_df$I[1] <- round(i0*N)
  SIR_df$S[1] <- N - SIR_df$I[1]
  
  for (t_num in seq_along(head(times, -1))){
    S = SIR_df$S[t_num]
    I = SIR_df$I[t_num]
    R = SIR_df$R[t_num]
    #
    newI = round(S * (1 - exp(-beta * I / N * dt)))
    newR = round(I * (1 - exp(-gamma * dt)))
    newC = rbinom(1, newI, prob = rho)
    #
    SIR_df$S[t_num + 1] = S - newI
    SIR_df$I[t_num + 1] = I + newI - newR
    SIR_df$R[t_num + 1] = R + newR
    SIR_df$newI[t_num] = newI
    SIR_df$newC[t_num] = newC
  }
  return(SIR_df)
}

true_pars = complete_pars(beta = true_beta, gamma = true_gamma)
true_df = run_SIR(true_pars)

require(RColorBrewer)

SIR_COLS = brewer.pal(4, 'Set1')[c(3, 1, 2, 4)]

obs_weeks = 1:8
obs_df <- true_df[which(true_df$time %in% obs_weeks), c("time", "newC")]

plot_sir = function(df, rho){
  time = df[['time']]
  S = df[['S']]
  I = df[['I']]
  R = df[['R']]
  newI = df[['newI']]
  
  obs_weeks = obs_df[['time']]
  #
  plot(time, S, type = 'l', xlab = 'Time', ylab = 'Population', ylim = c(0, max(S+I+R)), lwd = 2, col = SIR_COLS[1])
  lines(time, I, lwd = 2, col = SIR_COLS[2])
  lines(time, R, lwd = 2, col = SIR_COLS[3])
  #
  obs_locs <- which(time %in% obs_weeks)
  plot(time, newI, col = SIR_COLS[2], pch = 19)
  points(obs_df$time, obs_df$newC, col = SIR_COLS[4], pch = 4, lwd = 2)
  points(time[obs_locs], rho * newI[obs_locs], col = SIR_COLS[2], cex = 2, lwd = 2)
}

plot_likelihood <- function(rho, newI, newC, tol = 1e-1){
  prob_df = data.frame(obs = 0:newI,
                       prob = dbinom(0:newI, newI, prob = rho))
  prob_df$rel_prob = prob_df$prob / max(prob_df$prob)
  xmin <- max(min(min(which(prob_df$rel_prob > tol))-1, newC - 5), 0)
  xmax <- min(max(max(which(prob_df$rel_prob > tol)), newC + 5), newI)
  prob_df$keep <- 0
  prob_df$keep[xmin:xmax] <- 1
  prob_df$COL <- 1
  prob_df$COL[which(prob_df$obs == newC)] <- 2
  COLS <- c(rgb(0,0,0,.1), 2)
  barplot(prob_df$prob[prob_df$keep == 1], col = COLS[prob_df$COL[prob_df$keep == 1]])
}

get_ll = function(rho, df, obs_df){
  obs_weeks = obs_df[['time']]
  #
  newC_vec = obs_df[['newC']]
  newI_vec <- df[['newI']][which(df[['time']] %in% obs_weeks)]
  #
  L = prod(dbinom(newC_vec, newI_vec, prob = rho))
  ll = sum(dbinom(newC_vec, newI_vec, prob = rho, log = TRUE))
  #
  return(list(L = L, ll = ll))
}

plot_obs <- function(rho, df, obs_df){
  obs_weeks = obs_df[['time']]
  for (o_num in seq_along(obs_weeks)){
    tmp_newI <- df$newI[which(df$time == obs_weeks[o_num])]
    tmp_newC <- obs_df$newC[which(obs_df$time == obs_weeks[o_num])]
    plot_likelihood(rho, tmp_newI, tmp_newC)
  }
}


plot_Ls <- function(history){
  rho_vec <- history[['rho']]
  L_vec <- history[['L']]
  COLS <- rep(1, length(L_vec))
  PCHS <- rep(1, length(L_vec))
  COLS[which.max(L_vec)] <- 2
  PCHS[which.max(L_vec)] <- 19
  
  #
  plot(rho_vec, L_vec, xlim = c(0, 1),
       ylim = c(0, max(L_vec)), col = COLS, pch = PCHS)
}


plot_lls <- function(history){
  rho_vec <- history[['rho']]
  ll_vec <- history[['ll']]
  COLS <- rep(1, length(ll_vec))
  PCHS <- rep(1, length(ll_vec))
  COLS[which.max(ll_vec)] <- 2
  PCHS[which.max(ll_vec)] <- 19
  
  YMIN <- min(ll_vec[which(ll_vec > -Inf)])
  #
  plot(rho_vec, ll_vec, xlim = c(0, 1),
       ylim = c(YMIN, max(ll_vec)), col = COLS, pch = PCHS)
}


update_plot <- function(current, history, obs_df, get_mle = FALSE){
  panels = c(1, 3, 4, 5, 6, 1, 3, 4, 5, 6,
             1, 7, 8, 9, 10, 2, 7, 8, 9, 10,
             2, 11, 11, 12, 12, 2, 11, 11, 12, 12)
  
  if (get_mle){
    # 1 Find mle, punch that in for rho
    # 2 fill in the history with the whole likelihood and log-likelihood
  }
  layout(matrix(panels, 6, 5, byrow = TRUE),
         widths = c(3,1,1,1,1)) 
  par(mar=c(5.1,5.1,1.1,2.1), oma = c(0,0,3,2))
  plot_sir(current[['df']], current[['pars']][['rho']])
  par(mar=c(2.1,2.1,1.1,.1))  
  plot_obs(current[['pars']][['rho']], current[['df']], obs_df)
  #
  par(mar = c(5.1,2.1,2.1,.1))
  plot_Ls(history)
  plot_lls(history)
}

run_pars <- function(pars, obs_df){
  df = run_SIR(pars)
  ll = get_ll(pars[['rho']], df, obs_df)
  out <- c(ll, list(pars = pars, df = df))
  return(out)
}

init_best = function(init_pars, n_track, obs_df){
  df = run_SIR(init_pars)
  ll <- get_ll(init_pars[['rho']], df, obs_df)
  # 
  return(list(ll_vec = rep(NA, n_track),
              best = list(ll = ll, pars = init_pars, df = df)))
}

get_run_df <- function(run_list){
  rho <- run_list[['pars']][['rho']]
  L <- run_list[['L']]
  ll <- run_list[['ll']]
  #
  df <- data.frame(rho = rho, L = L, ll = ll)
  #
  return(df)
}

update_history <- function(current, history){
  current_df <- get_run_df(current)
  if (is.null(history)){
    history <- current_df
  } else {
    history <- rbind(history, current_df)  
  }
  return(history)
}

run_guess <- function(guess_pars, history, obs_df){
  current <- run_pars(guess_pars, obs_df)
  history <- update_history(current, history)
  update_plot(current, history, obs_df)
  return(history)
}

init_hist <- function(pars, obs_df){
  current <- run_pars(pars, obs_df)
  history <- get_run_df(current)
  return(history)
}

# Start with rho from previous page
init_rho = 0.5
history = init_hist(complete_pars(beta = guess_beta, 
                                  gamma = guess_gamma, 
                                  rho = init_rho), obs_df)
history = {}
history <- run_guess(complete_pars(rho = init_rho), history, obs_df)
############
# Start here
############


guess_rho = 0.2
history <- run_guess(complete_pars(rho = guess_rho), history, obs_df)
for (guess_rho in seq(0.01,.99, by = 0.01)){
  history <- run_guess(complete_pars(rho = guess_rho), history, obs_df)
  Sys.sleep(0.1)  # Pause for 0.1 seconds
  flush.console() # Force display
}






guess_beta = 2
guess_gamma = 1
guess_rho = 0.25


history <- run_guess(complete_pars(beta = guess_beta,
                                   gamma = guess_gamma,
                                   rho = guess_rho), history, obs_df)
