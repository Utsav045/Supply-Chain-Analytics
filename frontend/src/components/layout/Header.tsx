const Header = () => {
  return (
    <header className="app-header">
      <div className="header-title">
        <h1>Supply Chain Analytics</h1>
        <p>Monitor your supply chain performance</p>
      </div>

      <div className="header-actions">
        <div className="header-search">
          <span className="header-search-icon">⌕</span>
          <input
            type="text"
            placeholder="Search..."
            aria-label="Search"
          />
        </div>

        <button type="button" className="header-date">
          <span>▣</span>
          <span>Today</span>
        </button>

        <div className="header-profile">
          <div className="profile-avatar">P</div>

          <div className="profile-info">
            <span className="profile-name">Palak</span>
            <span className="profile-role">Administrator</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;